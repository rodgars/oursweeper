import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from game.use_cases import create_new_game, get_game_map_by_code, play_move, change_flag
from game.utils import deprecated_view


@require_POST
def new_game(request):
    """
    Create a new game with the specified number of rows, columns, and mines.

    Returns:
        JsonResponse: A JSON response containing the game code.

    Raises:
        JsonResponse: If the request body contains invalid JSON or missing required parameters.

    Payload Body Params:
        - rows (int): The number of rows in the game grid.
        - columns (int): The number of columns in the game grid.
        - mines (int): The number of mines in the game.

    Example Usage:
        POST /new_game
        {
            "rows": 10,
            "columns": 10,
            "mines": 20
        }

    Example Response:
        {
            "code": "ABC123"
        }
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not all(key in data for key in ("rows", "columns", "mines")):
        return JsonResponse({"error": "Missing required parameters"}, status=400)

    rows = int(data["rows"])
    columns = int(data["columns"])
    mines = int(data["mines"])

    game_code = create_new_game(rows, columns, mines)
    return JsonResponse({"code": game_code})


def game(request, game_code):
    """
    Retrieve the game map state for the given game code.

    Args:
        game_code (str): The code of the game to retrieve.

    Returns:
        JsonResponse: The JSON response containing the game map state.
    """
    game_map_state = get_game_map_by_code(game_code)
    return JsonResponse(game_map_state)


@deprecated_view
@require_POST
def move(request, game_code):
    """
    Process a move in the game. This move represents the user trying to reveal a cell.

    Args:
        game_code (str): The code of the game to make a move in.

    Returns:
        JsonResponse: The JSON response containing the game map state after the move.

    Raises:
        JsonResponse(status=400): If the request body contains invalid JSON.
        JsonResponse(status=400): If the required parameters (row and column) are missing.
        JsonResponse(status=400): If the move is invalid.

    Deprecated: This view is deprecated in favor of the WebSocket consumer.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not all(key in data for key in ("row", "column", "user")):
        return JsonResponse({"error": "Missing required parameters"}, status=400)

    row = int(data["row"])
    column = int(data["column"])
    user = data["user"]

    game_map_state = play_move(game_code, row, column, user)

    if game_map_state is None:
        return JsonResponse({"error": "Invalid move"}, status=400)

    return JsonResponse(game_map_state)


@deprecated_view
@require_POST
def flip_flag(request, game_code):
    """
    Flips the flag value of a cell in the game map.

    Args:
        game_code (str): The code of the game.

    Returns:
        JsonResponse: The JSON response containing the updated game map state.

    Raises:
        JsonResponse(status=400): If the request body contains invalid JSON.
        JsonResponse(status=400): If the required parameters (row and column) are missing.
        JsonResponse(status=400): If it can't flip the flag value.

    Deprecated: This view is deprecated in favor of the WebSocket consumer.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not all(key in data for key in ("row", "column", "user")):
        return JsonResponse({"error": "Missing required parameters"}, status=400)

    row = int(data["row"])
    column = int(data["column"])
    user = data["user"]

    game_map_state = change_flag(game_code, row, column, user)

    if game_map_state is None:
        return JsonResponse({"error": "Cannot flip flag value"}, status=400)
    return JsonResponse(game_map_state)
