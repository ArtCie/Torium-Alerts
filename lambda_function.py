from alerts_manager import AlertsManager


def lambda_handler(event, context):
    alerts_manager = AlertsManager()
    alerts_manager.process()

