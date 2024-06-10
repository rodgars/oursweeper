from datetime import datetime, timezone
from functools import lru_cache
import random
from django.db import transaction

from sqids import Sqids

from game.models import Cell, CellContent, Game, GameMapCurrentState, GameMapState

import logging
import sys

from game.tasks import create_game_event

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logger = logging.getLogger(__name__)


@lru_cache(maxsize=100)
def _convert_code_to_id(code: str) -> int:
    sqids = Sqids(min_length=6)
    return int(sqids.decode(code)[0])


def _create_empty_map(rows: int, cols: int) -> GameMapCurrentState:
    return [
        [
            CellContent(
                row=row,
                column=col,
                is_mine=False,
                is_revealed=False,
                is_flagged=False,
                adjacent_mines=0,
            )
            for col in range(cols)
        ]
        for row in range(rows)
    ]


def _create_initial_game_map(
    rows: int, cols: int, num_mines: int
) -> GameMapCurrentState:
    map = _create_empty_map(rows, cols)

    # Place mines randomly
    for _ in range(num_mines):
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        while map[row][col]["is_mine"]:  # If already a mine, re-pick
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)
        map[row][col]["is_mine"] = True

        # Increment adjacent cells
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < rows and 0 <= c < cols and map[r][c]["is_mine"] is False:
                    map[r][c]["adjacent_mines"] += 1

    return map


def _create_game_map_from_existing_game(game: Game) -> GameMapCurrentState:
    ongoing = game.state == "ongoing"
    cells = game.cells.all()

    map = _create_empty_map(game.rows, game.columns)

    for cell in cells:
        map[cell.row][cell.column]["is_revealed"] = cell.is_revealed
        map[cell.row][cell.column]["is_flagged"] = cell.is_flagged

        if ongoing and cell.is_revealed and not cell.is_flagged:
            map[cell.row][cell.column]["is_mine"] = cell.is_mine
            map[cell.row][cell.column]["adjacent_mines"] = cell.adjacent_mines

        if not ongoing:
            map[cell.row][cell.column]["is_mine"] = cell.is_mine
            if cell.is_revealed:
                map[cell.row][cell.column]["adjacent_mines"] = cell.adjacent_mines

    return map


def _get_game_by_code(code: str) -> Game:
    game_id = _convert_code_to_id(code)
    return Game.objects.prefetch_related("cells").get(id=game_id)


def _get_game_map(game: Game) -> GameMapState:
    game_map = _create_game_map_from_existing_game(game)

    delta_time = (game.ended_at or datetime.now(timezone.utc)) - game.created_at
    return GameMapState(
        map=game_map,
        state=game.state,
        code=game.code,
        started_at=game.created_at,
        total_time_in_seconds=delta_time.total_seconds(),
    )


def _ensure_win_condition(game: Game, row: int, column: int) -> bool:
    cells = game.cells.all()
    for cell in cells:
        if not cell.is_revealed and not cell.is_mine:
            return False
    return True


def _find_cell_by_position(game: Game, row: int, column: int) -> Cell | None:
    cells = game.cells.all()
    for cell in cells:
        if cell.row == row and cell.column == column:
            return cell
    return None


def _reveal_all_empty_cells(game: Game, row: int, column: int):
    cells_matrix = [[None] * game.columns for _ in range(game.rows)]
    cells = game.cells.all()
    for cell in cells:
        cells_matrix[cell.row][cell.column] = cell

    cells_to_update = []

    def reveal_empty_cell(cells_matrix, row, column):
        if cells_matrix[row][column].is_revealed:
            return
        cells_matrix[row][column].is_revealed = True
        cells_to_update.append(cells_matrix[row][column])

        if cells_matrix[row][column].adjacent_mines == 0:
            for r in range(row - 1, row + 2):
                for c in range(column - 1, column + 2):
                    if 0 <= r < game.rows and 0 <= c < game.columns:
                        reveal_empty_cell(cells_matrix, r, c)

    reveal_empty_cell(cells_matrix, row, column)
    return cells_to_update


def create_new_game(rows: int, columns: int, mines: int) -> str:
    with transaction.atomic():
        game = Game.objects.create(rows=rows, columns=columns, mines=mines)
        game_map = _create_initial_game_map(rows, columns, mines)
        cells = [
            Cell(
                game=game,
                row=row,
                column=column,
                is_mine=game_map[row][column]["is_mine"],
                adjacent_mines=game_map[row][column]["adjacent_mines"],
            )
            for row in range(rows)
            for column in range(columns)
        ]
        Cell.objects.bulk_create(cells)

    return game.code


def get_game_map_by_code(code: str) -> GameMapState:
    game = _get_game_by_code(code)
    return _get_game_map(game)


def play_move(code: str, row: int, column: int, user: str):
    game = _get_game_by_code(code)
    if game.state != "ongoing":
        return None

    cell = _find_cell_by_position(game, row, column)

    if not cell or cell.is_revealed or cell.is_flagged:
        return None

    cells_to_update = []

    with transaction.atomic():
        if cell.is_mine:
            game.state = "lost"
            game.ended_at = datetime.now(timezone.utc)
            game.save()

        if cell.adjacent_mines == 0:
            cells_to_update = _reveal_all_empty_cells(game, row, column)

        cell.is_revealed = True
        cells_to_update.append(cell)

        Cell.objects.bulk_update(cells_to_update, ["is_revealed"])

        if _ensure_win_condition(game, row, column):
            game.state = "won"
            game.ended_at = datetime.now(timezone.utc)
            game.save()

    create_game_event.delay(game.id, row, column, user)

    return _get_game_map(game)


def change_flag(code: str, row: int, column: int, user: str):
    game = _get_game_by_code(code)
    if game.state != "ongoing":
        return None

    cell = _find_cell_by_position(game, row, column)

    if not cell or cell.is_revealed:
        return None

    cell.is_flagged = not cell.is_flagged
    cell.save()

    create_game_event.delay(game.id, row, column, user)

    return _get_game_map(game)
