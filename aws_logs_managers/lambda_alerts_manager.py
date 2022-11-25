import re

from aws_logs_managers.aws_log_manager import AwsLogManager


class LambdaAlertsManager(AwsLogManager):
    def __init__(self):
        super().__init__()
        self.DISCORD_LINK = 'https://discord.com/api/webhooks/1045657207653535815' \
                            '/_hXxGly4ia2GVBKySZWRdXCNCGlIQZ_JMKq2hOrXBe1bjjfgjnj4pUv84MX8lihp2Z_7'
        self.QUERY_STRING = """fields @message"""

    def process_lambda_errors(self):
        lambda_log_groups = self.cloud_watch_manager.get_lambda_log_groups()
        for lambda_log_group in lambda_log_groups:
            title = lambda_log_group["logGroupName"][12:]
            lambda_logs = self.cloud_watch_manager.get_logs(lambda_log_group["logGroupName"], self.QUERY_STRING)
            errors = self._find_errors(lambda_logs, title)
            self.discord_manager.send_discord_messages(errors, self.DISCORD_LINK)

    def _find_errors(self, beanstalk_errors: dict, title: str):
        errors = []
        if beanstalk_errors.get('results'):
            local_index = 0
            beanstalk_errors = beanstalk_errors['results'][::-1]
            limit_index = len(beanstalk_errors)
            while local_index < limit_index:
                if self._look_for_critical_words(beanstalk_errors[local_index][0]['value']):
                    errors.append(self.discord_manager.prepare_discord_message(title, beanstalk_errors[local_index][0]['value']))
                local_index += 1
        return errors

    @staticmethod
    def _look_for_critical_words(message):
        return re.search(r'(LINE|CRITICAL|ERROR|WARNING)', message.upper())

