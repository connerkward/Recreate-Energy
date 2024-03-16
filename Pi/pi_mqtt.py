from awscrt import exceptions as awscrtexceptions, io, mqtt
from awsiot import mqtt_connection_builder
import time
import json
from datetime import datetime

# AWS MQTT CONFIG ---------------------------------------------
ENDPOINT = "a2kubfstl68fu2-ats.iot.us-west-2.amazonaws.com"
CLIENT_ID = "pi"
PATH_TO_CERTIFICATE = "certificates/f15c07ae8eb67c6adb1914e401f2bcad7d9f006f4b0b598614dcb2378177d311-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certificates/f15c07ae8eb67c6adb1914e401f2bcad7d9f006f4b0b598614dcb2378177d311-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/AmazonRootCA1.cer"

class MQTTConnection():
    """
    Connect with AWS MQTT IoT Core Broker. Supports publishing to topic, 
    and subscribing to topic with callback.
    """
    def __init__(self):
        self.connection = self.config()
        print("Connecting to {} with client ID '{}'...".format(
            ENDPOINT, CLIENT_ID))
        while True:
            try:
                connect_future = self.connection.connect()
                connect_future.result()  # Future.result() waits until a result is available
                break
            except awscrtexceptions.AwsCrtError:
                print("aws error. retrying...")
        print("Connected!")

    def config(self):
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
        """Publishes msg to topic. Appends datetime sent."""
        msg["datetime_published"] = datetime.now()
        self.connection.publish(topic=topic, payload=json.dumps(
            msg), qos=mqtt.QoS.AT_LEAST_ONCE)
        print("Published: '" + json.dumps(msg) +
            "' to : " + f"{topic}")


    def subscribe(self, topic, callback):
        """Subscribes to a topic and assigns a callback."""
        self.connection.subscribe(topic=topic, qos=mqtt.QoS.AT_MOST_ONCE, callback=callback)
        print("Subbed to the topic: " + topic)
        time.sleep(2)
    
    def disconnect(self):
        disconnect_future = self.connection.disconnect()
        disconnect_future.result()
