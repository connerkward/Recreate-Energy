from datetime import datetime
import boto3
from botocore.config import Config

# from QueryData import Query
from DatabaseManagement import DatabaseManagement
from QueryData import QueryData
from WriteData import WriteData

if __name__ == '__main__':

    session = boto3.Session() 

    write_client = session.client('timestream-write',
                                  config=Config(read_timeout=20,
                                                max_pool_connections=5000,
                                                retries={'max_attempts': 10}))

    query_client = session.client('timestream-query')

    # databaseManagement = DatabaseManagement(write_client)
    # queryManagement = Query(query_client)

    # databaseManagement.create_database()

    # databaseManagement.update_database()

    # databaseManagement.write_records()

    query_data = QueryData(query_client)
    write_data = WriteData(write_client)

    reactor_data = [
    {"datetime":"2022-05-21 05:05:52.040360","temp":"0","ph":"3.70","adcr":"430","adcv":"2099","dox":"29756","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:05:57.206260","temp":"0","ph":"4.62","adcr":"403","adcv":"1967","dox":"27885","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:06:02.410995","temp":"0","ph":"3.70","adcr":"437","adcv":"2133","dox":"30238","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:06:07.581690","temp":"0","ph":"4.38","adcr":"401","adcv":"1958","dox":"27757","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:06:12.767979","temp":"0","ph":"4.16","adcr":"433","adcv":"2114","dox":"29969","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:06:17.938986","temp":"0","ph":"4.05","adcr":"409","adcv":"1997","dox":"28310","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:06:23.099810","temp":"0","ph":"4.32","adcr":"420","adcv":"2050","dox":"29061","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:06:28.275927","temp":"0","ph":"3.92","adcr":"421","adcv":"2055","dox":"29132","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:06:33.468422","temp":"0","ph":"4.46","adcr":"414","adcv":"2021","dox":"28650","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:06:38.639437","temp":"0","ph":"3.81","adcr":"425","adcv":"2075","dox":"29416","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:06:43.820704","temp":"0","ph":"4.51","adcr":"411","adcv":"2006","dox":"28438","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:06:48.986667","temp":"0","ph":"3.76","adcr":"428","adcv":"2089","dox":"29614","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:06:54.180306","temp":"0","ph":"4.57","adcr":"408","adcv":"1992","dox":"28239","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:06:59.361985","temp":"0","ph":"3.70","adcr":"430","adcv":"2099","dox":"29756","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:07:04.539404","temp":"0","ph":"4.59","adcr":"406","adcv":"1982","dox":"28097","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:07:09.720804","temp":"0","ph":"3.65","adcr":"433","adcv":"2114","dox":"29969","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:07:14.907134","temp":"0","ph":"4.57","adcr":"405","adcv":"1977","dox":"28026","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:07:20.078205","temp":"0","ph":"3.65","adcr":"436","adcv":"2128","dox":"30167","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:07:25.253189","temp":"0","ph":"4.62","adcr":"401","adcv":"1958","dox":"27757","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:07:30.430672","temp":"0","ph":"3.89","adcr":"437","adcv":"2133","dox":"30238","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:07:35.596744","temp":"0","ph":"4.11","adcr":"402","adcv":"1962","dox":"27814","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:07:40.762653","temp":"0","ph":"4.27","adcr":"425","adcv":"2075","dox":"29416","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:07:45.938756","temp":"0","ph":"3.92","adcr":"421","adcv":"2055","dox":"29132","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:07:51.114893","temp":"0","ph":"4.49","adcr":"412","adcv":"2011","dox":"28508","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:07:56.285912","temp":"0","ph":"3.76","adcr":"428","adcv":"2089","dox":"29614","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:08:01.455922","temp":"0","ph":"4.59","adcr":"406","adcv":"1982","dox":"28097","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:08:06.622913","temp":"0","ph":"3.65","adcr":"435","adcv":"2124","dox":"30110","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:08:11.788832","temp":"0","ph":"4.65","adcr":"401","adcv":"1958","dox":"27757","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:08:16.970000","temp":"0","ph":"3.81","adcr":"437","adcv":"2133","dox":"30238","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:08:22.141184","temp":"0","ph":"4.27","adcr":"402","adcv":"1962","dox":"27814","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:08:27.317417","temp":"0","ph":"4.16","adcr":"433","adcv":"2114","dox":"29969","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:08:32.498646","temp":"0","ph":"4.00","adcr":"412","adcv":"2011","dox":"28508","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:08:37.664669","temp":"0","ph":"4.41","adcr":"416","adcv":"2031","dox":"28792","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:08:42.845914","temp":"0","ph":"3.78","adcr":"426","adcv":"2080","dox":"29487","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:08:48.022085","temp":"0","ph":"4.54","adcr":"409","adcv":"1997","dox":"28310","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:08:53.183025","temp":"0","ph":"3.68","adcr":"433","adcv":"2114","dox":"29969","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:08:58.359272","temp":"0","ph":"4.62","adcr":"403","adcv":"1967","dox":"27885","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:09:03.556652","temp":"0","ph":"3.68","adcr":"437","adcv":"2133","dox":"30238","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:09:08.743049","temp":"0","ph":"4.51","adcr":"401","adcv":"1958","dox":"27757","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:09:13.924409","temp":"0","ph":"4.05","adcr":"436","adcv":"2128","dox":"30167","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:09:19.085279","temp":"0","ph":"4.08","adcr":"405","adcv":"1977","dox":"28026","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:09:24.261564","temp":"0","ph":"4.30","adcr":"423","adcv":"2065","dox":"29274","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:09:29.437874","temp":"0","ph":"3.92","adcr":"421","adcv":"2055","dox":"29132","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:09:34.614007","temp":"0","ph":"4.46","adcr":"413","adcv":"2016","dox":"28579","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:09:39.795301","temp":"0","ph":"3.78","adcr":"426","adcv":"2080","dox":"29487","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:09:44.971478","temp":"0","ph":"4.54","adcr":"409","adcv":"1997","dox":"28310","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:09:50.142573","temp":"0","ph":"3.73","adcr":"429","adcv":"2094","dox":"29685","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:09:55.313581","temp":"0","ph":"4.57","adcr":"407","adcv":"1987","dox":"28168","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:10:00.503655","temp":"0","ph":"3.68","adcr":"432","adcv":"2109","dox":"29898","reactorid":"reactor1"},
    {"datetime":"2022-05-21 05:10:05.673008","temp":"0","ph":"4.62","adcr":"405","adcv":"1977","dox":"28026","reactorid":"reactor1"}
]



    print(write_data.write_records_with_common_attributes("pi", reactor_data))
    # print(query_data.get_reactor_data_hours_since_now("pi", 15)


