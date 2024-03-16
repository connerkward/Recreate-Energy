from typing import List, Set, Dict
import hashlib
from fastapi import WebSocket

# based on https://devcenter.heroku.com/articles/websocket-security

class WebsocketConnectionManager:
    """Manages websocket connections, and associated tokens, userID's."""
    def __init__(self):
        # {wsToken: [userID (sub), websocket]}
        self.tokens_and_active_connections_dict: Dict[str, List[str, WebSocket]] = {}
        # probably semantically better to use a dict rather than list
        # this would be a good use of time-based expiring JWT hashes

    def addToken(self, userID: str):
        # this is probably bad practice, adding a nonetype object as websocket.
        serial_salt = len(self.tokens_and_active_connections_dict) + 1 
        # TODO: replace this with cryptographically secure token
        # this is not salt, salt is random
        # this would be a good applicaiton expiring JWT's
        wsToken = hashlib.md5(bytes(userID, 'utf-8'), usedforsecurity=True).hexdigest() + f"-{serial_salt}"
        # token = len(wsManager.tokens_and_active_connections_dict) + 1 
        self.tokens_and_active_connections_dict.update({wsToken : [userID, None]})
        print(f"WS:\tWS CLIENT {wsToken} CREATED")
        return wsToken

    def getUserID(self, wsToken):
        assert self._check_token(wsToken)
        return self.tokens_and_active_connections_dict[wsToken][0]

    async def connect(self, websocket: WebSocket, wsToken: str):
        try:
            assert self._check_token(wsToken)
            userID = self.tokens_and_active_connections_dict[wsToken][0]
            self.tokens_and_active_connections_dict.update({wsToken : [userID, websocket]})
            print(f"WS:\tWS CLIENTS: {len(self.tokens_and_active_connections_dict.keys())}")
            print(f"WS:\tWS CLIENT {wsToken} CONNECTING...")
            await websocket.accept()
        except AssertionError:
            print("WS:\tFAILED, WSTOKEN NOT LISTED")
            print(f"WS:\tWS CLIENTS: {list(self.tokens_and_active_connections_dict.keys())}")

    async def disconnect(self, ws: WebSocket, wsToken: str):
        assert self._check_token(wsToken)
        websocket : WebSocket = self.tokens_and_active_connections_dict.pop(wsToken)[1]
        print(f"WS:\tWS CLIENTS: {list(self.tokens_and_active_connections_dict.keys())}")
        # await websocket.close()

    async def send(self, wsToken: str, json_msg: str):
        try:
            assert self._check_token(wsToken)
            await self.tokens_and_active_connections_dict[wsToken][1].send_json(json_msg)
            print(f"WS:\tSENT JSON TO CLIENT\n{json_msg}")
        except AssertionError or Exception:
            print(f"could not sent to {wsToken}")
            print(f"WS:\tWS CLIENTS: {list(self.tokens_and_active_connections_dict.keys())}")


    def get_userID_from_wsToken(self, wsToken:str):
        return [pair[0] for token, pair in self.tokens_and_active_connections_dict.items() if token ==wsToken]
    
    def get_pair_from_userID(self, userID:str):
        return [[token, pair] for token, pair in self.tokens_and_active_connections_dict.items() if pair[0] == userID]

    # async def broadcast(self, message: str):
    #     """Send to multiple websockets / users"""
    #     wsPairs = [self.get_pair_from_userID(userID) for userID in broadcast_to_userIDs]
    #     print(f"WS:\tBROADCAST CLIENTS: {wsPairs}")
    #     for token, pair in wsPairs:
    #         userID = pair[0]
    #         ws : WebSocket = pair[1]
    #         try:
    #             await ws.send_text(message)
    #             print(f"WS:\tWS SENT TO {userID}@{token}")
    #         except Exception as e:
    #             print("intended user does not have a websocket")
    #             print(e)

    async def receive(self, websocket: WebSocket, wsToken: str):
        assert self._check_token(wsToken)
        await websocket.receive()

    def _check_token(self, wsToken: str):
        if wsToken in self.tokens_and_active_connections_dict.keys():
            return True
        else:
            return False