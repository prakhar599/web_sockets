from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
from asgiref.sync import async_to_sync
import json


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print('WebSocket Connecting',event)
        print('Channel name is:' , self.channel_name)
        print('Channel layer is:' , self.channel_layer)
        
        try :
            async_to_sync(self.channel_layer.group_add)(
            'Mygroup',
            self.channel_name)
            print('added')
        
        except:
            print('Couldnt add in group')    
        
        self.send({
            'type':'websocket.accept'      
        })
        
    def websocket_receive(self,event):
        print('WebSocket receiving',event)
        
        try:
            async_to_sync(self.channel_layer.group_send)('Mygroup',{
                'type':'chat.message',
                'message':event['text']
            })
            print('message sent to group')
        except:
            print('Coudnt send msg to the group!')    
        
        try:
            def chat_message(self,event):
                self.send({
                    'type':'websocket.send',
                    'text': event['text']
                })
            print('message sent to clients')    
        except:
            print('Couldnt send msg to clients')        
            
    def websocket_disconnect(self,event):
        print('WebSocket disconnecting',event)
        async_to_sync(self.channel_layer.group_discard)(
        'Mygroup',
        self.channel_name
        )
        raise StopConsumer()
 
 
 
 
 
                

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print('WebSocket Connecting',event)
        
        await self.channel_layer.group_add(
        'Mygroup',
        self.channel_name)
        
        await self.send({
            'type': 'websocket.accept'
        })
        
    async def websocket_receive(self,event):
        print('WebSocket receiving',event['text'])
        await self.channel_layer.group_send('Mygroup',{
            'type':'chat.message',
            'message':event['text']
        })
        
        async def chat_message(self,event):
            await self.send({
                'type':'websocket.send',
                'text': event['text']
            })
            
    async def websocket_disconnect(self,event):
        print('WebSocket disconnecting',event)
        await self.channel_layer.group_discard(
        'Mygroup',
        self.channel_name
        ) 
        raise StopConsumer()               