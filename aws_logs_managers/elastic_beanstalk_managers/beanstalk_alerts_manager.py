import re

from aws_logs_managers.aws_log_manager import AwsLogManager


class BeanstalkAlertsManager(AwsLogManager):
    def __init__(self):
        super().__init__()
        self.DISCORD_LINK = "https://discord.com/api/webhooks/1044291586118398002/Bue-iseH3k-I6SJLjDyJ_ZO5ALwYakJiXJW" \
                            "-_mQvgqpdAdZ7DFNwH1W7bylzNaLINi8e"
        self.LOG_GROUP = "/aws/elasticbeanstalk/Torium-api/var/log/web.stdout.log"
        self.QUERY_STRING = "fields @message"
        self.TITLE = "**TORIUM API ALERT**"
        self.errors = []

    def process_beanstalk_errors(self):
        beanstalk_errors = self.cloud_watch_manager.get_logs(self.LOG_GROUP, self.QUERY_STRING)
        self._find_errors(beanstalk_errors)
        self.discord_manager.send_discord_messages(self.errors, self.DISCORD_LINK)

    def _find_errors(self, beanstalk_errors: dict):
        if beanstalk_errors.get('results'):
            local_index = 0
            beanstalk_errors = beanstalk_errors['results'][::-1]
            limit_index = len(beanstalk_errors)
            while local_index < limit_index:
                if self._look_for_critical_words(beanstalk_errors[local_index][0]['value']):
                    error_stream, local_index = self._collect_error_stream(local_index, limit_index, beanstalk_errors)
                    self.errors.append(self.discord_manager.prepare_discord_message(self.TITLE, error_stream))
                local_index += 1
    @staticmethod
    def _look_for_critical_words(message):
        return re.search(r'(LINE|CRITICAL|ERROR|WARNING)', message.upper())

    def _parse_log(self, log_record: str):
        timestamp = log_record[:log_record.find(' ip')]
        log_string = log_record[log_record.find('web: ') + 5:]
        return timestamp, log_string

    def _collect_error_stream(self, local_index, limit_index, beanstalk_errors):
        timestamp, _ = self._parse_log(beanstalk_errors[local_index][0]['value'])
        single_log = timestamp + "\n"
        while local_index < limit_index:
            timestamp, message = self._parse_log(beanstalk_errors[local_index][0]['value'])
            single_log += message + "\n"
            local_index += 1
            if "INFO" in message.upper():
                break
        return single_log, local_index

