from aws_logs_managers.db_alerts_manager import DbAlertsManager
from aws_logs_managers.elastic_beanstalk_managers.health_alerts_manager import HealthAlertsManager


class AlertsManager:
    def __init__(self):
        self._db_alerts_manager = DbAlertsManager()
        self._health_alerts_manager = HealthAlertsManager()

    def process(self):
        self._db_alerts_manager.process_db_errors()
        self._health_alerts_manager.process_health_errors()