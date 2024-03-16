from TimeStream.Constant import DATABASE_NAME, ONE_GB_IN_BYTES, TABLE_NAME


import boto3
from datetime import datetime, timezone

class QueryData:
    def __init__(self, client=boto3.Session().client(
        'timestream-query', 
        region_name='us-west-2',
        aws_access_key_id="AKIAXZWQXYQSYHFTUFMU",
        aws_secret_access_key="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"
    )):
        self.client = client
        self.paginator = client.get_paginator('query')

    # See records ingested into this table so far
    # SELECT_ALL = f"SELECT * FROM {DATABASE_NAME}.{TABLE_NAME}"

    # queries = [SELECT_ALL]

    # def run_all_queries(self):
    #     for query_id in range(len(self.queries)):
    #         # print(
    #         #     "Running query [%d] : [%s]"
    #         #     % (query_id + 1, self.queries[query_id])
    #         # )
    #         self.run_query(self.queries[query_id])

    def run_query(self, query_string):
        try:
            page_iterator = self.paginator.paginate(QueryString=query_string)
            result = []
            [[result.append(row) for row in self._parse_query_result(page)] for page in page_iterator]
            [print(d, "\n") for d in result]
            return result
        except Exception as err:
            print("Exception while running query:", err)

    def _parse_query_result(self, query_result) -> list:
        query_status = query_result["QueryStatus"]

        # progress_percentage = query_status["ProgressPercentage"]
        # print(f"Query progress so far: {progress_percentage}%")

        # bytes_scanned = (
        #     float(query_status["CumulativeBytesScanned"]) / ONE_GB_IN_BYTES
        # )
        # print(f"Data scanned so far: {bytes_scanned} GB")

        # bytes_metered = (
        #     float(query_status["CumulativeBytesMetered"]) / ONE_GB_IN_BYTES
        # )
        # print(f"Data metered so far: {bytes_metered} GB")

        column_info = query_result['ColumnInfo']
        # print("Metadata: %s" % column_info)
        return [self._parse_row(column_info, row) for row in query_result['Rows']]

    def _parse_row(self, column_info, row):
        data = row['Data']
        row_output = {}
        for j in range(len(data)):
            info = column_info[j]
            datum = data[j]
            k,v = self._parse_datum(info, datum)
            row_output[k] = v
        return row_output

    def _parse_datum(self, info, datum):
        if datum.get('NullValue', False):
            return ("%s=NULL" % info['Name'],)

        column_type = info['Type']

        # If the column is of TimeSeries Type
        if 'TimeSeriesMeasureValueColumnInfo' in column_type:
            return self._parse_time_series(info, datum)

        # If the column is of Array Type
        elif 'ArrayColumnInfo' in column_type:
            array_values = datum['ArrayValue']
            return info['Name'], self._parse_array(info['Type']['ArrayColumnInfo'], array_values)

        # If the column is of Row Type
        elif 'RowColumnInfo' in column_type:
            row_column_info = info['Type']['RowColumnInfo']
            row_values = datum['RowValue']
            return self._parse_row(row_column_info, row_values)

        # If the column is of Scalar Type
        else:
            return info['Name'], datum['ScalarValue']

    def _parse_time_series(self, info, datum):
        time_series_output = []
        for data_point in datum['TimeSeriesValue']:
            time_series_output.append(
                "{time=%s, value=%s}"
                % (
                    data_point['Time'],
                    self._parse_datum(
                        info['Type']['TimeSeriesMeasureValueColumnInfo'],
                        data_point['Value'],
                    ),
                )
            )
        return "[%s]" % str(time_series_output)

    def _parse_array(self, array_column_info, array_values):
        array_output = []
        for datum in array_values:
            array_output.append(self._parse_datum(array_column_info, datum))

        return "[%s]" % str(array_output)

    # def run_query_with_multiple_pages(self, limit):
    #     query_with_limit = self.SELECT_ALL + " LIMIT " + str(limit)
    #     print("Starting query with multiple pages : " + query_with_limit)
    #     self.run_query(query_with_limit)

    # def cancel_query(self):
    #     print("Starting query: " + self.SELECT_ALL)
    #     result = self.client.query(QueryString=self.SELECT_ALL)
    #     print("Cancelling query: " + self.SELECT_ALL)
    #     try:
    #         self.client.cancel_query(QueryId=result['QueryId'])
    #         print("Query has been successfully cancelled")
    #     except Exception as err:
    #         print("Cancelling query failed:", err)

    def get_reactor_data(self, reactor_common_name, start_time, end_time):
        '''
        start_time and end_time must be string and in the following ISO format
        "2020-10-10 9:00:00"
        '''
        sd = datetime.fromisoformat(start_time).replace(tzinfo=timezone.utc)
        ed = datetime.fromisoformat(end_time).replace(tzinfo=timezone.utc)
        # *NIX time
        # sts = str(int(round(sd.timestamp()) * 1000))
        # ets = str(int(round(ed.timestamp()) * 1000))

        # adding qoutes cause aws is weird
        sdstr = f"'{sd}'"
        edstr = f"'{ed}'"
        QUERY = f'SELECT * FROM "05312022-reactor-data"."reactor-{reactor_common_name}" where time between {sdstr} and {edstr}'
        result = self.run_query(QUERY)
        return result

    def get_reactor_data_hours_before_now(self, reactor_common_name, hours_since_now):
        '''
        start_time and end_time must be string and in the following ISO format
        "2020-10-10 9:00:00"
        '''
        QUERY = f'SELECT * FROM {DATABASE_NAME}."reactor-{reactor_common_name}" WHERE time between ago({hours_since_now}h) AND now()'
        self.run_query(QUERY)

    @staticmethod
    def _parse_column_name(info):
        if 'Name' in info:
            return info['Name'] + "="
        else:
            return ""
