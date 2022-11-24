from aws_logs_managers.aws_log_manager import AwsLogManager


class AccessAlertsManager(AwsLogManager):
    def __init__(self):
        super().__init__()
        self.DISCORD_LINK = 'https://discord.com/api/webhooks/1045437993525190717' \
                            '/3Vlj_fKPiuCENNesArlsT5unKgKbP_gBEngaz34Fq7kn41NOI00UryowBodqZy2OjZoJ'
        self.LOG_GROUP = '/aws/elasticbeanstalk/Torium-api/var/log/nginx/access.log'
        self.TITLE = "**ACCESS ERROR**"
        self.QUERY_STRING = """fields @message
 | parse @message '* - - [*] "*" * *' as ip, date, method, code
 | display ip, date, method, rest, code"""

    def process_access_errors(self):
        access_logs = self.cloud_watch_manager.get_logs(self.LOG_GROUP, self.QUERY_STRING)
        errors = self._find_errors(access_logs)
        self.discord_manager.send_discord_messages(errors, self.DISCORD_LINK)

    def _find_errors(self, access_logs: dict):
        if access_logs.get('results'):
            errors = []
            for log in access_logs['results']:
                if self._check_message_code(log[3]['value']):
                    description = self._build_description(log)
                    errors.append(self.discord_manager.prepare_discord_message(self.TITLE, description))
            return errors

    @staticmethod
    def _check_message_code(code):
        return code != '200'

    def _build_description(self, log_data):
        location = self.ip_tracker.get_location(log_data[0]['value'])
        return f"""Date: {log_data[1]['value']}
IP: {log_data[0]['value']} - located in {location['city']} - {location['region']} - {location['country']}
Executed HTTP method: {log_data[2]['value']}
**CODE {log_data[3]['value']}**
"""
