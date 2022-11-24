from ip_tracker import IpTracker
from discord_manager import DiscordManager
from cloud_watch_manager import CloudWatchManager


class DbAlertsManager:
    def __init__(self, cloud_watch_manager: CloudWatchManager, ip_tracker: IpTracker, discord_manager: DiscordManager):
        self.DISCORD_LINK = 'https://discord.com/api/webhooks/1044294790516318229' \
                            '/M0v6CLui8b2z6PBpXP24xuvoChBxOrlIZ_u34PRyj0djPuLCcy8vlDI_IQb87rbgTzjc'
        self.LOG_GROUP = '/aws/rds/instance/toddy-test/postgresql'
        self.QUERY_STRING = """fields @message
            | parse @message "* * *:*:*:[*]:*:*" as date, time, timezone, ipaddress, dbuser, pid, type, text
            | display date, time, timezone, ipaddress, dbuser, pid, type, text"""
        self.TITLE = "**DATABASE ERROR**"
        self.ip_tracker = ip_tracker
        self.discord_manager = discord_manager
        self.cloud_watch_manager = cloud_watch_manager

    def process_db_errors(self):
        database_logs = self.cloud_watch_manager.get_logs(self.LOG_GROUP, self.QUERY_STRING)
        errors = self._find_errors(database_logs)
        self.discord_manager.send_discord_messages(errors, self.DISCORD_LINK)

    def _find_errors(self, database_logs: dict):
        if database_logs.get('results'):
            errors = []
            for log in database_logs['results']:
                if self._check_message_type(log[6]['value']):
                    description = self._build_description(log)
                    errors.append(self.discord_manager.prepare_discord_message(self.TITLE, description))
            return errors

    @staticmethod
    def _check_message_type(type):
        return type in ['ERROR', 'WARNING', 'FATAL', 'DETAIL']

    def _build_description(self, log_data):
        location = self.ip_tracker.get_location(log_data[3]['value'][:log_data[3]['value'].find('(')])
        return f"""Date: {log_data[0]['value']}  Time: {log_data[1]['value']} {log_data[2]['value']}
IP: {log_data[3]['value']} - located in {location['city']} - {location['region']} - {location['country']}
User {log_data[4]['value']} pid: {log_data[5]['value']}
**{log_data[6]['value']}: {log_data[7]['value']}**
"""
