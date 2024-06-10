from django.db import models
from sqids import Sqids
from typing import Literal, TypedDict


class CellContent(TypedDict):
    row: int
    column: int
    is_mine: bool
    is_revealed: bool
    is_flagged: bool
    adjacent_mines: int


GameEventsType = Literal[
    "reveal mine", "flag cell", "unflag cell", "reveal cell", "reveal last cell - win"
]


GameMapCurrentState = list[list[CellContent]]


class GameMapState(TypedDict):
    map: GameMapCurrentState
    state: str
    code: str
    started_at: str
    total_time_in_seconds: float


class Game(models.Model):
    rows = models.PositiveIntegerField()
    columns = models.PositiveIntegerField()
    mines = models.PositiveIntegerField()
    state = models.CharField(max_length=10, default="ongoing")  # ongoing, won, lost
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True)

    @property
    def code(self):
        sqids = Sqids(min_length=6)
        return sqids.encode([self.id])


class Cell(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="cells", related_query_name="cell"
    )
    row = models.PositiveIntegerField()
    column = models.PositiveIntegerField()
    is_mine = models.BooleanField(default=False)
    is_revealed = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    adjacent_mines = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["game", "row", "column"], name="unique_cell"
            )
        ]


class GameEvents(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="events",
        related_query_name="event",
    )
    row = models.PositiveIntegerField()
    column = models.PositiveIntegerField()
    event = models.CharField(
        max_length=50
    )  # reveal mine, flag cell, unflag cell, reveal cell, reveal last cell - win
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=50)
