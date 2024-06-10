from celery import shared_task

from game.models import GameEvents, Cell


# TODO: Investigate retrying the task if it fails, logging the error
@shared_task
def create_game_event(game_id: int, row: int, column: int, user: str):
    cell = Cell.objects.select_related("game").get(
        game_id=game_id, row=row, column=column
    )
    game = cell.game

    event = "reveal last cell - win"
    if cell.is_mine:
        event = "reveal mine"
    elif cell.is_flagged:
        event = "flag cell"
    elif not cell.is_flagged:
        event = "unflag cell"
    elif cell.is_revealed and game.state == "ongoing":
        event = "reveal cell"

    GameEvents.objects.create(
        game_id=game_id, row=row, column=column, event=event, user=user
    )
