#!/usr/bin/python
# This script can run on raspberrypi and also pretend to be a raspberrypi
from datetime import datetime
import json
import threading
import time 
import serial

import pi_mqtt as mqtt
import pi_serial as serial
import pi_localdb as localdb

# SENSOR CONFIG ----------------------------------------------------
SENSOR_READING_ATTR_TUPLES = [
    ("datetime", "Timestamp"),
    ("temp", "Temperature"),
    ("ph", "pH"),
    ("adcr", "ADC Raw"),
    ("adcv", "ADC Voltage)"),
    ("dox", "Dissolved Oxygen")
]  # sensor reading keys and display names
SENSOR_READING_ATTR_DICT = dict(SENSOR_READING_ATTR_TUPLES)  # dict version

# MSG TIMING CONFIG ---------------------------------------------
# PASSIVE_MSG_SECONDS = 10  # how often to send messages in passive mode
ACTIVE_MSG_SECONDS = 5  # how often to send messages in active mode
TIMESTREAM_UPDATE_MINUTES = 10  # how often to send updates to timestream
LOCAL_DB_UPDATE_SECONDS = 10   # how often to send updates to local db

# MQTT CONFIG -------------------------------
assigned_userID = "6faea729-0214-49d7-9afe-1553af585653" # TEMP
REACTORID = "reactor1"
COMMANDS_SUBSCRIBE_TOPIC = f"/users/{assigned_userID}/commands" # one user can send a command that is consumed by multiple reactors.
STATES_PUBLISH_TOPIC = f"/reactors/{REACTORID}/states" # reactor in active mode publishes it's state
COMMAND_CONFIRMATION_PUBLISH_TOPIC = f"/reactors/{REACTORID}/commands-recieved" # confirmed list from the reactor of commands it has recieved.

SEND_CONFRIMATION = False

class SensorThread(threading.Thread):
    """    
    This thread is constantly reading serial sensor readings.
    It updates the local database and publishes to MQTT if
    the active mode flag is set.
    """
    def __init__(self, serial_conn, mqtt_conn, localdb_conn,active_mode=False):
        threading.Thread.__init__(self)
        self.event = threading.Event() # when event occurs, thread ends.
        self.active_mode = active_mode
        self.mqttconn = mqtt_conn
        self.serialconn = serial_conn
        self.localdb = localdb_conn # set this way because sqlite3 must be used in same thread.

    def run(self):
        """
        Gets sensor readings and if in active mode, publishes. 
        Blocking. Runs forever while event flag is not set.
        """
        while not self.event.is_set():
            sensor_reading = self.serialconn.readline()
            sensor_reading = SensorThread._append_reactorID(sensor_reading)
            
            self.localdb.add_sensor_reading(sensor_reading)
            if self.active_mode:
                print(f"ACTIVE: {sensor_reading}")
                self.mqttconn.publish(STATES_PUBLISH_TOPIC, sensor_reading)
            else:
                print(f"PASSIVE: {sensor_reading}")
            time.sleep(ACTIVE_MSG_SECONDS)

    def _append_reactorID(sensor_reading: dict):
        """Helper, adds reactor related info to sensor reading."""
        sensor_reading["reactorid"] = REACTORID # TODO: Update, maybe with Thing ID?
        return sensor_reading


def start():
    """    
    Connects to serial, mqtt. Adds a callback to MQTT subscribe
    that can turn active mode on or off, as well as getting a 
    single serial sensor reading.
    """
    try: 
        # pre-emptively open serial, mqtt, localdb connections
        active_thread = None
        mqtt_connection = mqtt.MQTTConnection()
        serial_connection = serial.SerialConnection()
        localDB_connection = localdb.LocalDB()

        # Start sensor reading thread
        active_thread = SensorThread(serial_connection, mqtt_connection, localDB_connection)
        active_thread.start()

        def mqtt_subscribe_callback(topic, payload, dup, qos, retain, **kwargs):
            # topic (str): Topic receiving message.
            # payload (bytes): Payload of message.
            # dup (bool): DUP flag. If True, this might be re-delivery of an earlier attempt to send the message.
            # qos (QoS): Quality of Service used to deliver the message.
            # retain (bool): Retain flag. If True, the message was sent as a result of a new subscription being made by the client.
            # **kwargs (dict): Forward-compatibility kwargs.
            # if dup: # message may be a duplicate
            #   return 
            # NOTE: uses closures for mqtt, serial, localdb connections, 
            # which is why this function is in this location. 
            
            payload = json.loads(payload.decode('utf-8'))

            print(f"COMMAND RECIEVED: {payload}")
            
            if payload["command_type"] == "active":
                if payload["command_value"] == "start":
                    active_thread.active_mode = True
                elif payload["command_value"] == "stop":
                    active_thread.active_mode = False
            elif payload["command_type"] == "get":
                sensor_reading = serial_connection.readline()
                mqtt_connection.publish(STATES_PUBLISH_TOPIC, sensor_reading)
            elif payload["command_type"] == "set": # TODO: command values for actuators. 
                setcommand_response = serial_connection.send_command(payload["command_value"]) # ex, {peltier1 : 1} # ON
                # if setcommand_response: # TODO: if setcommand_response == good
                #     sensor_reading = serial_connection.readline() # TODO: sensor readings should include actuator state.
                #     mqtt_connection.publish(STATES_PUBLISH_TOPIC, sensor_reading)
                mqtt_connection.publish(STATES_PUBLISH_TOPIC, setcommand_response)
            
            if SEND_CONFRIMATION:
                payload["datetime_recieved"] = datetime.now()
                payload["recieved_by"] = REACTORID
                mqtt_connection.publish(COMMAND_CONFIRMATION_PUBLISH_TOPIC, payload)

        # await MQTT commands
        mqtt_connection.subscribe(COMMANDS_SUBSCRIBE_TOPIC, mqtt_subscribe_callback)
       
        # loop forever until exit, listening for mqtt commands
        while True: 
            pass

    except KeyboardInterrupt:
        print(" exiting...")
        if active_thread:
            active_thread.event.set()
        mqtt_connection.disconnect()
        serial_connection.disconnect()
        exit()

if __name__ == '__main__':
    start()
