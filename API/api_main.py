# FastAPI auto generates documentation and Postman-like interface for testing API.
# FastAPI is Flask-like, and is built on Starlette.
# To run with auto reload, uvicorn api_main:app --reload
# Or without auto reload, run this file
import asyncio
from fastapi import Depends, FastAPI, HTTPException, status, WebSocketDisconnect, Request
from api_ws import WebsocketConnectionManager
import api_aws as aws
import uvicorn
from starlette.websockets import WebSocket, WebSocketState
from typing import Optional, Any
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from datetime import datetime
from random import randint
from typing import List
import boto3
from botocore.config import Config
from TimeStream.QueryData import QueryData

# NOTES
# Url path could also include userID and/or reactorID.
# It is considered best REST practice to include such information
# in both the request body AND url path.
# However, for security purposes, it is likely better to not include
# any identifiying information in the URL as it is likely being logged
# either by DNS or local servers.

# AWS Cognito "access code" was chosen over "ID code" because it contains no user information. 

# CONFIG ======================================================
MQTT_COMMAND_TOPIC_FUNC = lambda userID : f"/users/{userID}/commands" # commands are associated with user
MQTT_STATE_TOPIC_FUNC = lambda reactorID : f"/reactors/{reactorID}/states" # states associated with reactor
MQTT_STATE_TOPIC_FUNC = lambda reactorID : f"/reactors/{reactorID}/commands-recieved" # if confirmation flag was sent in command msg
# confirmationflagged because if default, number of msg's increases by 50%

# STARTUP =====================================================
cognito_conn = aws.CognitoConnection()
app = FastAPI()
wsManager = WebsocketConnectionManager()
mqtt_conn = aws.MQTTConnection()
timestream_conn = QueryData()

# CORS ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SCHEMAS =====================================================
class CommandJSON(BaseModel):
    reactorID: str 
    command_type: str
    command_value: Any

class ReactorStateJSON(BaseModel):
    ph: str
    temp: str
    dox: str
    adcv: str
    adcr: str

VALID_SENSORS = {"temp", "ph", "adcr", "adcv", "dox"}
VALID_COMMAND_TYPES_VALUES = {
    "active" :{"start", "stop"}, 
    "get": VALID_SENSORS.union({"_"}),
    "set": VALID_SENSORS.union({"_"}),
    "query": {"_"}
    } # "_" means all for sensors

# HTTP ========================================================
@app.get("/", include_in_schema=False)
async def root():
    """
    Can redirect the root ("/") to the /docs url, but in ECS, Load Balancer does health 
    checks on / so for this retun 200 OK.
    """
    #return RedirectResponse(url='/docs') # debug only (causes error with AWS health checker)
    return {"message": "Hello Health Checker! For API Documentation, navigate to /docs ."}

@app.get("/api/user/token", tags=["User"])
async def authenticate(username, password):
    """
    TODO: DEBUG ONLY -> Remove for production!
    Authenticates a users credentials, return token. This should only be used for debug.
    Production flow should be: frontend cognito login->returns token->token is used in API calls
    testuser, DingoDingo123*
    """
    try:
        access_token, id_token = aws.CognitoConnection.authenticate(username, password)
        return {"access_token": access_token, "id_token": id_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/api/user/userID", tags=["User"])
async def get_user_ID(current_user: aws.AccessUser = Depends(cognito_conn.auth.claim(aws.AccessUser))):
    """
    Returns userID for a given AWS Cognito acces token.
    """
    try:
        return current_user.sub
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to get user info.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
@app.get("/api/user/reactors", tags=["User"])
async def get_user_reactors(request: Request, current_user: aws.AccessUser = Depends(cognito_conn.auth.claim(aws.AccessUser))):
# async def get_user_reactors():
    """
    Returns associated reactors for a given userID. 
    """
    api_key = request.headers["authorization"].split(" ")[1] # get api access token from headers
    # ^ there is probably a better way to do this
    return cognito_conn.get_reactors(current_user.username, api_key)

# # GETTING DATA ========================
@app.post("/api/reactor/range", tags=["Reactor"])
async def get_sensor_data_range(
    request: Request,
    commandJSON: CommandJSON,
    current_user: aws.AccessUser = Depends(cognito_conn.auth.claim(aws.AccessUser))
    ):
    """
    GET request for requesting sensor data from Cloud database (AWS Timestream).
    Not yet implemented.
    """
    # validate commandJSON: {reactorID: str, command_type:"query", command_value:{datetime_start: datetime, datetime_end: datetime}}
    commandJSONdict = dict(commandJSON)
    if commandJSONdict["command_type"] != "query":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad command type.")
    if not cognito_conn.validate_reactor_by_name(
        reactor_common_name=commandJSONdict["reactorID"],
        username=current_user.username,
        token=request.headers["authorization"].split(" ")[1],
        ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not associated with reactor.")

    # TODO: validate datetimes
    start_datetime = commandJSONdict["command_value"]["datetime_start"] 
    end_datetime = commandJSONdict["command_value"]["datetime_end"]
    
    # TODO: REQUEST FROM TIMESTREAM (previous API)
    # reactor_time_series_data = get_reactor_data(start_datetime, end_datetime, reactor_name)
    result = timestream_conn.get_reactor_data(commandJSONdict["reactorID"], start_datetime, end_datetime)
    if result == None:
        return []
    # Changing some results for data consistency
    for row in result:
        row.pop("measure_name")
        row["datetime"] = row.pop("time")
        
    return result


# POSTING REACTOR COMMANDS ===========
@app.post("/api/reactor/command", tags=["Reactor"])
async def post_command(
    request: Request,
    commandJSON: CommandJSON,
    current_user: aws.AccessUser = Depends(cognito_conn.auth.claim(aws.AccessUser))
    ):
    """
    POST request for sending commands to the Pi over MQTT. Sending to /{userID}/commands
    """
    commandJSONdict = dict(commandJSON)
    if not cognito_conn.validate_reactor_by_name(
        reactor_common_name=commandJSONdict["reactorID"],
        username=current_user.username,
        token=request.headers["authorization"].split(" ")[1],
        ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not associated with reactor.") 
    commandJSONdict["userID"] = current_user.sub
    if commandJSONdict["command_type"] not in VALID_COMMAND_TYPES_VALUES.keys():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad command type.")
    if commandJSONdict["command_value"] not in VALID_COMMAND_TYPES_VALUES[commandJSONdict["command_type"]]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad command value.")
    topic = MQTT_COMMAND_TOPIC_FUNC(commandJSONdict["userID"])
    mqtt_conn.publish(topic=topic, msg=commandJSONdict)
    command_type = commandJSONdict["command_type"].upper()
    command_value = commandJSONdict["command_value"].upper()
    reactorID = commandJSONdict["reactorID"]
    return {"command_type": command_type, "command_value": command_value, "published_to":topic, "reactorID": reactorID}


# WEBSOCKET ENDPOINT (LIVE DATA) ==================================
@app.get("/api/reactor/active-read", tags=["Reactor"])
async def get_active_read_url(current_user: aws.AccessUser = Depends(cognito_conn.auth.claim(aws.AccessUser))):
    """
    GET request for websocket token, which is used to determine url.
    WebSocket url, using a hash based on userID and an appended connection number.
    """
    try:
        wsToken = wsManager.addToken(current_user.sub) 
        print(f"WS USER {wsToken} ADDED")
        return {"token": wsToken, "path":f"/api/reactor/ws/{wsToken}"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to get info.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    



@app.websocket("/api/reactor/ws/{wsToken}")
async def websocket_endpoint(websocket: WebSocket, wsToken: str):
    """
    WebSocket, opens websocket and mqtt on connect and relays messages 
    TODO: some kind of filtering of the MQTT messages so that only correct user recieves readings 
    REQUIRES "ASSOCIATED_REACTORS"
    """
    reactorID = "reactor1" # TODO: REMOVE DEBUG ONLY REQUIRES "ASSOCIATED_REACTORS"
    try:
        await wsManager.connect(websocket, wsToken)
        await wsManager.send(wsToken, {"msg": "CONNECTED", "type": "alert"}) # somehow this is required to keep the connection alive? 
        print(f"WS USER {wsToken} CONNECTED")
        def sub_callback(topic, payload, dup, qos, retain, **kwargs):
            # topic (str): Topic receiving message.
            # payload (bytes): Payload of message.
            # dup (bool): DUP flag. If True, this might be re-delivery of an earlier attempt to send the message.
            # qos (QoS): Quality of Service used to deliver the message.
            # retain (bool): Retain flag. If True, the message was sent as a result of a new subscription being made by the client.
            # **kwargs (dict): Forward-compatibility kwargs.

            json_payload = json.loads(payload.decode('utf-8'))
            print(f"SENDING JSON TO WS CLIENTS...")
            asyncio.run(wsManager.send(wsToken, {"msg": json_payload, "type": "reactor_state"})) # used to run async function in sync callback
            print("SENT")

        # TODO: subscribe to all associated reactors
        topic = f"/reactors/{reactorID}/states"
        mqtt_conn.subscribe(topic=topic, callback=sub_callback)
        print(f"MQTT:\tSubscribed {topic}")
        while websocket.client_state == WebSocketState.CONNECTED:
            # this is kind of a hacky cheeseball way
            # to keep constant looping that doesnt block the program
            await wsManager.receive(websocket, wsToken) 
        await wsManager.disconnect(websocket, wsToken)
    except Exception or KeyboardInterrupt: # this is bad form
        await wsManager.disconnect(websocket, wsToken)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
