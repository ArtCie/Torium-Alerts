import boto3
from aws_logs_managers.aws_log_manager import AwsLogManager


class HealthAlertsManager(AwsLogManager):
    def __init__(self):
        super().__init__()
        self.cloud_watch_health_client = boto3.client(
            service_name='elasticbeanstalk',
            region_name='eu-central-1'
        )
        self.TITLE = "**HEALTH ALERT**"
        self.DISCORD_LINK = 'https://discord.com/api/webhooks/1045431411231956994/2pEZ0' \
                            '-gMoQhwSHMBs3IJSHnmndPDhBEmxiLHzMhqQlYvetXqOqI9CYKTMnkbqsOk4S5I'
        self.errors = []

    def process_health_errors(self):
        response = self.cloud_watch_health_client.describe_environments()
        for item in response['Environments']:
            env_name = item['EnvironmentName']
            health_state = item['HealthStatus']
            if health_state != "Ok":
                health_response = self.cloud_watch_health_client.describe_environment_health(
                    EnvironmentName=env_name,
                    AttributeNames=['Causes']
                )
                health_causes = health_response['Causes']
                message = self._build_description(env_name, health_causes)
                self.errors.append(self.discord_manager.prepare_discord_message(self.TITLE, message))
        self.discord_manager.send_discord_messages(self.errors, self.DISCORD_LINK)

    def _build_description(self, env_name, health_causes):
        message = "**Found Errors In:" + env_name + "\n**"
        message += "Causes: ".join(health_causes) + "\n\n"
        return message
