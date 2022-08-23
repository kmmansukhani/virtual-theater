import json
from tkinter.font import names
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from . models import *
from django.db.models import Q


class WaitingRoomConsumer(WebsocketConsumer):

    def connect(self):
        self.party_id = self.scope["url_route"]["kwargs"]["party_id"]
        self.room_group_name = 'waitingroom_%s' % self.party_id

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        username = text_data_json["username"]
        user_id = text_data_json["user_id"]
        usernames = User.objects.filter(party_id=self.party_id).filter(~Q(user_id=user_id)).values_list('username', flat=True)
        print(usernames)
        for name in usernames:
            self.send(text_data=json.dumps({
                'username': name
            }))
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'waitingroom_username',
                'username': username
            }
        )

    def waitingroom_username(self, event):
        username = event['username']
        self.send(text_data=json.dumps({
            'username': username
        }))