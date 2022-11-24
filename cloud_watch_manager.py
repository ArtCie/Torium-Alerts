import time

import boto3


class CloudWatchManager:
    def __init__(self):
        self.client = boto3.client('logs',
                                   region_name='eu-central-1'
                                   )
        self._current_time = int(time.time())

    def get_logs(self, log_group, query_string):
        start_query_response = self.client.start_query(
            logGroupName=log_group,
            startTime=self._current_time - 12000,
            endTime=self._current_time,
            queryString=query_string
        )
        query_id = start_query_response['queryId']
        response = None
        while response is None or response['status'] == 'Running' or response['status'] == 'Scheduled':
            time.sleep(2)
            response = self.client.get_query_results(queryId=query_id)
        return response
