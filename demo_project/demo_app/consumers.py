from channels.generic.websocket import WebsocketConsumer
import json
class NotificationConsumer(WebsocketConsumer):
     def connect(self):
        self.accept()
        self.channel_layer.group_add("notification_group", self.channel_name)
        self.send(text_data=json.dumps({
            'type':'connection success',
            'message':'connected'
        }))


     def disconnect(self, close_code):
        self.channel_layer.group_discard("notification_group", self.channel_name)

     def receive(self, text_data):
        pass
