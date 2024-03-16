import sqlite3

# SENSOR CONFIG ---------------------------------
SENSOR_READING_ATTR_TUPLES = [
    ("datetime", "Timestamp"),
    ("temp", "Temperature"),
    ("ph", "pH"),
    ("adcr", "ADC Raw"),
    ("adcv", "ADC Voltage)"),
    ("dox", "Dissolved Oxygen")
]  # sensor reading keys and display names
SENSOR_READING_ATTR_DICT = dict(SENSOR_READING_ATTR_TUPLES)  # dict version

# LOCAL DB CONFIG -----------------------------
DB_NAME = 'readings.db'
TABLE_NAME = "vitals"
SQL_FIELDS = [key for key, _ in SENSOR_READING_ATTR_TUPLES]

class LocalDB():
    def __init__(self, log=True) -> None:
        """Uses sensor readings defined in pi_main to create local SQLiteDB if not existing. Connects."""
        self.log = log # flag for debug
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        sql_create_table = 'create table if not exists ' + \
        TABLE_NAME + f' ({", ".join(SQL_FIELDS)})'
        self.conn.execute(sql_create_table)

    def add_sensor_reading(self, sensor_reading: dict):
        """
        Uses sensor readings display strings defined in pi_main. 
        Inserts param sensor_reading dict into DB.
        """
        sql_values = [sensor_reading[key]
                for key in SENSOR_READING_ATTR_DICT.keys()]
        sql_insert = f"INSERT INTO vitals({','.join(SQL_FIELDS)}) VALUES({str(sql_values).strip('[]')})"
        self.conn.execute(sql_insert)
        
    def disconnect(self):
        self.conn.close()