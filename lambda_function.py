from discord_manager import DiscordManager
from cloud_watch_manager import CloudWatchManager
from ip_tracker import IpTracker

from db_alerts_manager import DbAlertsManager


def lambda_handler(event, context):
    cloud_watch_manager = CloudWatchManager()
    discord_manager = DiscordManager()
    ip_tracker = IpTracker()

    db_alerts_manager = DbAlertsManager(cloud_watch_manager, ip_tracker, discord_manager)
    db_alerts_manager.process_db_errors()
