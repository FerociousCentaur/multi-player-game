from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json
from channels.layers import get_channel_layer
from collections import defaultdict
from .models import Game

class GameRoom(WebsocketConsumer):
    # def __init__(self):
    #     self.channel_layer = get_channel_layer()
    #groups = ["broadcast"]
    room_connection_counts = defaultdict(lambda: 0)
    def connect(self):
        #print('hello')
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        print(self.scope['url_route']['kwargs'])
        self.room_group_name = 'room_%s' %  self.room_name
        print(self.room_group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.room_connection_counts[self.room_name] += 1
        print("connected No of players", self.room_connection_counts[self.room_name])
        
    def disconnect(self,erro_code):
        #pass
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.room_connection_counts[self.room_name] -= 1
        print("No of players", self.room_connection_counts[self.room_name])
        if self.room_connection_counts[self.room_name]==0:
            game = Game.objects.get(room_code=self.room_name)
            players = game.players.all()
            for player in players:
                player.delete()
            game.delete()
        
    def receive(self , text_data):
        #self.send(text_data="Hello world!")
        print(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type' : 'run_game',
                'payload' : text_data
            }
        )

        
    
    def run_game(self , event):
        data = event['payload']
        data = json.loads(data)

        self.send(text_data= json.dumps({
            'payload' : data['data']
        }))

         