
# from mimetypes import init
from awscrt import exceptions as awscrtexceptions, io, mqtt
from awsiot import mqtt_connection_builder
import json
from pycognito import Cognito as CognitoKey
from fastapi_cloudauth.cognito import Cognito as CognitoVerify

from pydantic import BaseModel
import time
import boto3
from botocore.config import Config
# TODO: Production flow should be: frontend cognito login->returns token->token is used in API calls


# TODO: Bad practice. replace with ENV or similar 
# this really should not be on the git

# AWS CONFIG ---------------------------------------------
REGION = "us-west-2"

# AWS MQTT CONFIG ---------------------------------------------
ENDPOINT = "a2kubfstl68fu2-ats.iot.us-west-2.amazonaws.com"
CLIENT_ID = "api"
PATH_TO_CERTIFICATE = "certificates/a5874f452db517015b7839d9e6a83bc770d26b16f9fc6f822577a55fa3c5dec8-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certificates/a5874f452db517015b7839d9e6a83bc770d26b16f9fc6f822577a55fa3c5dec8-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/AmazonRootCA1.cer"

# AWS COGNITO CONFIG ------------------------------------------
COGNITO_USERPOOLID = 'us-west-2_lUFRBpitK'
COGNITO_DEBUG_CLIENTID = "4u1top7i4u8g2063149c09bum8" # server cognito app client cliendID
COGNITO_CLIENTID = "451j19u9vqba8rf3pknm5o59mq" # frontend cognito app client cliendID
COGNITO_DEBUG_SECRET = "170n5hl45p6s4uq7h99n7r2fvjlbep819qet3soak1roqtivc0s"
COGNITO_ASSOCIATED_REACTORS_KEY = "profile"

# AWS COGNITO  ------------------------------------------
# https://pypi.org/project/pycognito/
# some default user cognito login credentials
# testuser, DingoDingo123*


class AccessUser(BaseModel):
    """A Cognito User"""
    sub: str
    username: str


class CognitoConnection():
    def __init__(self) -> None:
        self.auth = CognitoVerify(
            region=REGION,
            userPoolId=COGNITO_USERPOOLID,
            client_id=COGNITO_CLIENTID
        )
    
    def authenticate(username, password):
        """TODO: DEBUG ONLY: Returns AWS Cognito access token."""
        u = CognitoKey(COGNITO_USERPOOLID, COGNITO_DEBUG_CLIENTID, client_secret=COGNITO_DEBUG_SECRET,
                    username=username)
        u.authenticate(password=password)
        return u.access_token, u.id_token

    def get_reactors(self, username, token):
        # right now duct tape solution -> stored as string of a python set in attribute 'profile'
        userdata = CognitoKey(
            COGNITO_USERPOOLID,
            COGNITO_DEBUG_CLIENTID, 
            username=username,
            client_secret=COGNITO_DEBUG_SECRET,
            access_token=token,
            ).get_user()
        # print(userdata._data[COGNITO_ASSOCIATED_REACTORS_KEY])
        # COGNITO_ASSOCIATED_REACTORS_KEY
        # 'profile' key being used temporarily to store "associated reactors" ARNs
        # as string representation with commas ("thingID, thingID,") then eval'ed into a python set
        # hacky solution but it is simpler than making another database
        profile_str = userdata._data[COGNITO_ASSOCIATED_REACTORS_KEY]
        associated_reactor_thing_ARNs = eval(profile_str)
        associated_reactor_things = [{"name": ARN.split("/")[-1], "ARN": ARN} for ARN in associated_reactor_thing_ARNs]
        return associated_reactor_things

    def validate_reactor_by_name(self, reactor_common_name, username, token):
        # right now duct tape solution -> stored as string of a python set in attribute 'profile'
        userdata = CognitoKey(
            COGNITO_USERPOOLID,
            COGNITO_DEBUG_CLIENTID, 
            username=username,
            client_secret=COGNITO_DEBUG_SECRET,
            access_token=token,
            ).get_user()
        # print(reactor_common_name)
        # print(username)
        # print(userdata._data)
        # COGNITO_ASSOCIATED_REACTORS_KEY
        # 'profile' key being used temporarily to store "associated reactors" ARNs
        # as string representation with commas ("thingID, thingID,") then eval'ed into a python set
        # hacky solution but it is simpler than making another database
        profile_str = userdata._data[COGNITO_ASSOCIATED_REACTORS_KEY]
        associated_reactor_thing_common_names = [val.split("/")[-1] for val in eval(profile_str)]
        # print(associated_reactor_thing_common_names)
        if reactor_common_name in associated_reactor_thing_common_names:
            return True
        return False

# AWS MQTT  ------------------------------------------
class MQTTConnection():
    """
    Connect with AWS MQTT IoT Core Broker. Supports publishing to topic, 
    and subscribing to topic with callback.
    """

    def __init__(self):
        self.connection = self.config()
        print(f"MQTT:\tConnecting to AWS over MQTT...")
        while True:
            try:
                connect_future = self.connection.connect()
                connect_future.result()  # Future.result() waits until a result is available
                break
            except awscrtexceptions.AwsCrtError as e:
                print("\t\taws error. retrying...") # sometimes aws throws a strange error and wont connect at first
                print(e)
            time.sleep(5)
        print("\tConnected to AWS over MQTT!")

    def config(self):
        # config resources
        event_loop_group = io.EventLoopGroup(1)
        host_resolver = io.DefaultHostResolver(event_loop_group)
        client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
        mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
        )
        return mqtt_connection

    def publish(self, topic, msg):
        message = msg
        self.connection.publish(topic=topic, payload=json.dumps(
                message), qos=mqtt.QoS.AT_LEAST_ONCE)
        print("MQTT:\tPublished COMMAND To " + topic)
        print(f"\t{json.dumps(message)}")

    def subscribe(self, topic, callback):
        print("MQTT:\tSubbed to the topic: " + topic)
        return self.connection.subscribe(
            topic=topic, qos=mqtt.QoS.AT_MOST_ONCE, callback=callback)

    def disconnect(self):
        disconnect_future = self.connection.disconnect()
        disconnect_future.result()

# AWS Timestream DB  ------------------------------------------
class TimestreamConnection():
    def __init__(self) -> None:
        # session = boto3.Session()
        # self.write_client = session.client('timestream-write',
        #                         config=Config(read_timeout=20,
        #                                     max_pool_connections=5000,
        #                                     retries={'max_attempts': 10}))

        # self.query_client = session.client('timestream-query')
        # queryManagement = Query(query_client)
        # databaseManagement.create_database()
        # databaseManagement.update_database()
        # databaseManagement.write_records()
        pass

    def create_database(self):
        # print("Creating Database")
        pass

    def describe_database(self):
        # print("Describing Database")
        pass

    def update_database(self, kms_id):
        # print("Updating database")
        pass
        # try:
        #     result = self.client.update_database(
        #         DatabaseName=Constant.DATABASE_NAME, KmsKeyId=kms_id)
        #     print("Database [%s] was updated to use kms [%s] successfully" % (Constant.DATABASE_NAME,
        #                                                                       result['Database']['KmsKeyId']))
        # except self.client.exceptions.ResourceNotFoundException:
        #     print("Database doesn't exist")
        # except Exception as err:
        #     print("Update database failed:", err)

if __name__ == '__main__':
    tsc = TimestreamConnection()