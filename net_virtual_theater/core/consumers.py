import json
from tkinter import W
from channels.generic.websocket import AsyncWebsocketConsumer
from . models import *
from django.db.models import Q
from channels.db import database_sync_to_async


class WaitingRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.party_id = self.scope["url_route"]["kwargs"]["party_id"]
        self.room_group_name = 'waitingroom_%s' % self.party_id

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if self.username:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'waitingroom_username',
                    'to_remove': True,
                    'username': self.username
                }
            )
        '''
        if self.user_id:
            usernames = await database_sync_to_async(self.get_all_usernames)(self.user_id)
            if len(usernames) == 0:
                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                )
        '''
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # self.close()

    def get_all_usernames(self, user_id):
        usernames = User.objects.filter(party_id=self.party_id).filter(
            ~Q(user_id=user_id)).values_list('username', flat=True)
        return list(usernames)

    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        self.username = text_data_json["username"]
        self.user_id = text_data_json["user_id"]
        usernames = await database_sync_to_async(self.get_all_usernames)(self.user_id)
        for name in usernames:
            await self.send(text_data=json.dumps({
                'username': name
            }))
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'waitingroom_username',
                'to_remove': False,
                'username': self.username
            }
        )

    async def waitingroom_username(self, event):
        await self.send(text_data=json.dumps({
            'toRemove': event['to_remove'],
            'username': event['username']
        }))
