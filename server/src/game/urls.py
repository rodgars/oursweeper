from django.urls import path

from . import views

urlpatterns = [
    path("new", views.new_game, name="new_game"),
    path("<str:game_code>", views.game, name="game"),
    path("<str:game_code>/move", views.move, name="move"),
    path("<str:game_code>/flip_flag", views.flip_flag, name="flip_flag"),
]
