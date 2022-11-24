from discord_manager import DiscordManager
from cloud_watch_manager import CloudWatchManager
from ip_tracker import IpTracker


class AwsLogManager:
    def __init__(self):
        self.cloud_watch_manager = CloudWatchManager()
        self.discord_manager = DiscordManager()
        self.ip_tracker = IpTracker()
