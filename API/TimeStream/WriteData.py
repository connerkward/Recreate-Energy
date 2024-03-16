from multiprocessing.dummy import Array
import Constant
import boto3
import time
from datetime import datetime, timezone

class WriteData:
    def __init__(self, client=boto3.Session().client('timestream-query', region_name='us-west-2')):
        self.client : boto3.Session = client

    def write_records_with_common_attributes(self, reactor: str, sensor_reading_dicts: list):
        # assumes example sensor reading dict schema:
        # {adcr: "435", adcv: "2124", datetime: "2022-05-31 22:12:06.552043", dox: "42", ph: "3.73", reactorid: "reactor1", temp: "0"}
        def gen_state_record(sensor_reading: dict):
            # print(time.mktime(datetime.fromisoformat(sensor_reading.pop("datetime")).timetuple()))
            d = datetime.fromisoformat(sensor_reading.pop("datetime")).replace(tzinfo=timezone.utc)
            ts = str(int(round(d.timestamp()) * 1000))
            r = sensor_reading.pop("reactorid")

            return {
            "Dimensions": [{'Name': 'reactorID', 'Value': str(r)}],
            'MeasureName': 'state',
            'Time': ts,
            "MeasureValueType": "MULTI",
            "MeasureValues": [{"Name": str(sensor), "Value": str(float(value)), "Type": "DOUBLE"} for sensor,value in sensor_reading.items()]
            }

        records = [gen_state_record(l) for l in sensor_reading_dicts]
        print(records)
        try:
            result = self.client.write_records(DatabaseName=Constant.DATABASE_NAME, TableName=f"reactor-{reactor}",
                                               Records=records, CommonAttributes={})
            print("WriteRecords Status: [%s]" % result['ResponseMetadata']['HTTPStatusCode'])
        except self.client.exceptions.RejectedRecordsException as err:
            self._print_rejected_records_exceptions(err)
        except Exception as err:
            print("Error:", err)
    
    @staticmethod
    def _current_milli_time():
        return str(int(round(time.time() * 1000)))

