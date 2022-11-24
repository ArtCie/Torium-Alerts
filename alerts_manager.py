from aws_logs_managers.db_alerts_manager import DbAlertsManager


class AlertsManager:
    def __init__(self):
        self._db_alerts_manager = DbAlertsManager()

    def process(self):
        self._db_alerts_manager.process_db_errors()