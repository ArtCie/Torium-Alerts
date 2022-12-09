import datetime
from threading import Thread

from aws_logs_managers.db_alerts_manager import DbAlertsManager
from aws_logs_managers.lambda_alerts_manager import LambdaAlertsManager
from aws_logs_managers.elastic_beanstalk_managers.health_alerts_manager import HealthAlertsManager
from aws_logs_managers.elastic_beanstalk_managers.access_alerts_manager import AccessAlertsManager
from aws_logs_managers.elastic_beanstalk_managers.beanstalk_alerts_manager import BeanstalkAlertsManager
from aws_logs_managers.lambda_response_manager import LambdaResponseManager


class AlertsManager:
    def __init__(self):
        self._db_alerts_manager = DbAlertsManager()
        self._lambda_alerts_manager = LambdaAlertsManager()
        self._health_alerts_manager = HealthAlertsManager()
        self._access_alerts_manager = AccessAlertsManager()
        self._beanstalk_alerts_manager = BeanstalkAlertsManager()
        self._lambda_response_manager = LambdaResponseManager()

    def process(self):
        threads = [
            Thread(target=self._db_alerts_manager.process_db_errors),
            Thread(target=self._lambda_alerts_manager.process_lambda_errors),
            Thread(target=self._health_alerts_manager.process_health_errors),
            Thread(target=self._access_alerts_manager.process_access_errors),
            Thread(target=self._beanstalk_alerts_manager.process_beanstalk_errors),
            Thread(target=self._lambda_response_manager.process_lambda_response)
        ]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
