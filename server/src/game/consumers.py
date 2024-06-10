from datetime import datetime
from urllib.parse import parse_qs
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.cache import cache

from game.use_cases import change_flag, play_move


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.game_code = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = f"game_{self.game_code}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        self.accept()

        query_string = self.scope["query_string"].decode()
        self.user = parse_qs(query_string).get("user", [None])[0]
        connected_users = cache.get(self.game_code, [])
        if self.user not in connected_users:
            connected_users.append(self.user)
        cache.set(self.game_code, connected_users)

        # Broadcast connected users list to group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "user.list", "users": connected_users}
        )

    def disconnect(self, close_code):
        user = self.user
        connected_users = cache.get(self.game_code, [])
        if user in connected_users:
            connected_users.remove(user)
        cache.set(self.game_code, connected_users)

        # Broadcast connected users list to group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "user.list", "users": connected_users}
        )

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        error_message = None

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            error_message = {"error": "Invalid JSON"}

        if not all(key in data for key in ("row", "column", "user", "type")):
            error_message = {"error": "Missing required parameters"}

        if error_message:
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(self.group_name, error_message)
            return

        row = int(data["row"])
        column = int(data["column"])
        user = data["user"]
        type = data["type"]

        game_map_state = None
        if type == "flag":
            game_map_state = change_flag(self.game_code, row, column, user)
        elif type == "reveal":
            game_map_state = play_move(self.game_code, row, column, user)

        if game_map_state is None:
            return

        # Convert datetime.datetime objects to strings
        game_map_state = {
            k: v.isoformat() if isinstance(v, datetime) else v
            for k, v in game_map_state.items()
        }

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "update.map", "map": game_map_state}
        )

    def update_map(self, event):
        self.send(text_data=json.dumps(event))

    def user_list(self, event):
        self.send(text_data=json.dumps(event))
