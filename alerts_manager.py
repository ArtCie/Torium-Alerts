from discord_manager import DiscordManager
from cloud_watch_manager import CloudWatchManager
from ip_tracker import IpTracker

from aws_logs_managers.db_alerts_manager import DbAlertsManager


class AlertsManager:
    def __init__(self):
        self.cloud_watch_manager = CloudWatchManager()
        self.discord_manager = DiscordManager()
        self.ip_tracker = IpTracker()

        self._db_alerts_manager = DbAlertsManager(self.cloud_watch_manager, self.ip_tracker, self.discord_manager)

    def process(self):
        self._db_alerts_manager.process_db_errors()