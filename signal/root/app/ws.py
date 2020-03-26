import websockets
import json
import os
import logging


async def send_message(message: str):
    response = "Something bad happened" 
    try:
        uri = os.environ.get("HA_WEBSOCKET", "ws://supervisor/core/websocket")
        logging.info(f'Sending message to {uri}')
        async with websockets.connect(uri) as websocket:

            logging.info(f'Connecting to websocket')
            await websocket.recv()
            logging.info(f'Connected to websocket')

            await websocket.send(json.dumps({
                "type": "auth",
                "access_token": os.environ.get("SUPERVISOR_TOKEN")
            }))
            auth_response = json.loads(await websocket.recv())
            logging.info(f'Authenticated to websocket')
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
                        logging.error(f'did not receive an expected response from home assistant {conversation_response}')
                else:
                    logging.error(f'unexpected response {conversation_response}')
            else:
                logging.error(f'could not authenticate with home assistant {auth_response}')
    except Exception as e:
        logging.error(f'Unexpected error {e}')
    return response
