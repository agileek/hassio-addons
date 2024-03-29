import websockets
import json
import os
import logging

async def send_message(ha_websocket: str, access_token: str, message: str):
    response = "Something bad happened" 
    try:
        logging.info(f'Sending message to {ha_websocket}')
        async with websockets.connect(ha_websocket) as websocket:

            logging.debug(f'Connecting to websocket')
            await websocket.recv()
            logging.debug(f'Connected to websocket')

            await websocket.send(json.dumps({
                "type": "auth",
                "access_token": access_token
            }))
            auth_response = json.loads(await websocket.recv())
            logging.debug(f'Authenticated to websocket')
            if "type" in auth_response and auth_response["type"] == "auth_ok":
                await websocket.send(json.dumps({
                    "id": 1,
                    "type": "conversation/process",
                    "text": message,
                }))
                conversation_response = json.loads(await websocket.recv())
                logging.debug(f'response {conversation_response}')
                if "type" in conversation_response and "success" in conversation_response:
                    if conversation_response["success"] and conversation_response["type"] == "result":
                        response = conversation_response.get("result", {}).get("response", {}).get("speech", {}).get("plain", {}).get("speech")
                        if response is None:
                            logging.warning('did not receive an intelligible response from home assistant {conversation_response}')
                    else:
                        logging.error('did not receive an expected response from home assistant')
                else:
                    logging.error(f'unexpected response {conversation_response}')
            else:
                logging.error(f'could not authenticate with home assistant {auth_response}')
    except Exception:
        logging.exception('Unexpected error')
    return response