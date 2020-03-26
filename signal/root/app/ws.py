import asyncio
import websockets
import json
import os


async def send_message(message: str):
    uri = os.environ.get("HA_WEBSOCKET", "http://supervisor/core/websocket")
    async with websockets.connect(uri) as websocket:
        response = "Something bad happened"
        await websocket.recv()
        await websocket.send(json.dumps({
            "type": "auth",
            "access_token": os.environ.get("SUPERVISOR_TOKEN")
        }))
        auth_response = json.loads(await websocket.recv())
        if "type" in auth_response and auth_response["type"] == "auth_ok":
            await websocket.send(json.dumps({
                "id": 1,
                "type": "conversation/process",
                "text": message,
            }))
            conversation_response = json.loads(await websocket.recv())
            if "type" in conversation_response and "success" in conversation_response:
                if conversation_response["success"] and conversation_response["type"] == "result":
                    response = conversation_response['result']['speech']['plain']['speech']
                else:
                    print(f'did not receive an expected response from home assistant {conversation_response}')
            else:
                print(f'unexpected response {conversation_response}')
        else:
            print(f'could not authenticate with home assistant {auth_response}')
        return response
