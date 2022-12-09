import boto3
import json
from threading import Thread

from aws_logs_managers.aws_log_manager import AwsLogManager


class LambdaResponseManager(AwsLogManager):
    def __init__(self):
        super().__init__()
        self.DISCORD_LINK = 'https://discord.com/api/webhooks/1050660912425607229/UgsFbOgs8ZhE6QWhPmhGZkchf_WOjid' \
                            '-oHiXcL2fNnwkOSC6fqUv3o78Da8dm90BZYZB'
        self.TITLE = 'Execute alerts'
        self.color = 3468099
        self.lambda_execute_threads = []
        self.lambda_client = boto3.client('lambda', region_name='eu-central-1')
        self.results = []

    def process_lambda_response(self):
        lambda_names = self.lambda_client.get_paginator('list_functions')
        for func_page in lambda_names.paginate():
            for func in func_page['Functions']:
                if 'amplify' not in func['FunctionName']:
                    self.lambda_execute_threads.append(Thread(target=self._execute_function, args=[func['FunctionName']]))
        [thread.start() for thread in self.lambda_execute_threads]
        [thread.join() for thread in self.lambda_execute_threads]
        discord_message = self.discord_manager.prepare_discord_message(self.TITLE, '\n'.join(self.results), color=self.color)
        self.discord_manager.send_discord_messages([discord_message], self.DISCORD_LINK)

    def _execute_function(self, function_name: str):
        response = self.lambda_client.invoke(
            FunctionName=function_name,
            Payload=json.dumps({'test': 'test'}),
        )
        parsed_response = json.loads(response['Payload'].read())
        text_response = self._valid_response(function_name, parsed_response)
        self.results.append(text_response)

    def _valid_response(self, function_name: str, parsed_response: dict):
        if parsed_response.get('statusCode') != 200:
            self.color = 14177041
            return f"{function_name} -> ERROR: error_type - {parsed_response['errorType']} - error_message: {parsed_response['errorMessage']}"
        return f"{function_name} - SUCCESS"
