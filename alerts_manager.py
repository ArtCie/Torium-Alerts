from aws_logs_managers.db_alerts_manager import DbAlertsManager
from aws_logs_managers.lambda_alerts_manager import LambdaAlertsManager
from aws_logs_managers.elastic_beanstalk_managers.health_alerts_manager import HealthAlertsManager
from aws_logs_managers.elastic_beanstalk_managers.access_alerts_manager import AccessAlertsManager
from aws_logs_managers.elastic_beanstalk_managers.beanstalk_alerts_manager import BeanstalkAlertsManager


class AlertsManager:
    def __init__(self):
        self._db_alerts_manager = DbAlertsManager()
        self._lambda_alerts_manager = LambdaAlertsManager()
        self._health_alerts_manager = HealthAlertsManager()
        self._access_alerts_manager = AccessAlertsManager()
        self._beanstalk_alerts_manager = BeanstalkAlertsManager()

    def process(self):
        self._db_alerts_manager.process_db_errors()
        self._lambda_alerts_manager.process_lambda_errors()
        self._health_alerts_manager.process_health_errors()
        self._access_alerts_manager.process_access_errors()
        self._beanstalk_alerts_manager.process_beanstalk_errors()
