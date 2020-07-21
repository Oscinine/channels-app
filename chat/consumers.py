from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json

class ChatConsumer(AsyncWebsocketConsumer):
	#Accepts connection from client
	async def connect(self):
		#Use channels to synchronize data in channel
		await self.channel_layer.group_add(
			'chat',
			self.channel_name
		)
		await self.accept()
	
	#Receive data from client
	async def receive(self, text_data):
		#Send to client directly
		'''
		text_data_json = json.loads(text_data)
		text_data_json['message'] += ' echo'
		self.send(json.dumps(text_data_json))
		'''

		#Send to channel layer instead
		await self.channel_layer.group_send(
				'chat',
				{
					'type': 'chat_message',
					'message': text_data
				}
			)

	async def chat_message(self, event):
		message = event['message']
		await self.send(text_data=message)

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
				'chat',
				self.channel_name
			)