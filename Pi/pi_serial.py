import serial
import time
# import asyncio
from datetime import datetime
from pi_main import SENSOR_READING_ATTR_TUPLES, SENSOR_READING_ATTR_DICT
# ARDUINO CONFIG ---------------------------------------------
SERIAL_PORT = '/dev/ttyACM0' # raspbian linux
# SERIAL_PORT = 'COM4'  # windows
# SERIAL_PORT = "/dev/tty.usbmodem11401"  # Mac M1
SERIAL_BAUD = 9600

class SerialConnection:
    def __init__(self) -> None:
        # ARDUINO CONNECT ======================================
        # establish serial either windows or linux
        while True:
            try:
                self.conn = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1)
                # clear serial terminal
                self.conn.flush()
                break
            except serial.serialutil.SerialException: 
                print("waiting for serial...")
                time.sleep(5)
                

    def _readline(self):
        # Read serial and convert to data
        line = self.conn.readline().decode('utf-8').rstrip()
        line_data = line.split(',')
        sensor_reading = {
            SENSOR_READING_ATTR_TUPLES[0][0]: str(datetime.now()), 
            SENSOR_READING_ATTR_TUPLES[1][0]: line_data[0], 
            SENSOR_READING_ATTR_TUPLES[2][0]: line_data[1], 
            SENSOR_READING_ATTR_TUPLES[3][0]: line_data[2], 
            SENSOR_READING_ATTR_TUPLES[4][0]: line_data[3], 
            SENSOR_READING_ATTR_TUPLES[5][0]: line_data[4]}
        return sensor_reading

    def readline(self):
        while True:
            try:
                if self.conn.in_waiting > 0:
                    try:
                        sensor_reading = self._readline()
                    except IndexError or KeyError:
                        # print("Incomplete serial message.")
                        pass
                    else:
                        return sensor_reading
            except OSError:
                print("Serial disconnected. Attempting reconnect.")
                while True:
                    try:
                        self.conn = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1)
                        # clear serial terminal
                        self.conn.flush()
                        break
                    except serial.serialutil.SerialException: 
                        print("waiting for serial...")
                        time.sleep(5)
    
    def send_command(self, command_value: dict):
        while True:
            try:
                if self.conn.in_waiting > 0:
                    # TODO: send commands over serial
                    self.conn.write(f'{command_value}'.encode('utf-8')) # TODO: UNTESTED!
                    # TODO: maybe read from serial to see what pi returns 
                    return self.conn.readline()
            except OSError:
                print("Serial disconnected. Attempting reconnect.")
                while True:
                    try:
                        self.conn = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1)
                        # clear serial terminal
                        self.conn.flush()
                        break
                    except serial.serialutil.SerialException: 
                        print("waiting for serial...")
                        time.sleep(5)
    
    def disconnect(self):
        self.conn.close()