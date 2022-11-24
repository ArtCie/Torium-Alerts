from aws_logs_managers.aws_log_manager import AwsLogManager


class HealthAlertsManager(AwsLogManager):
    def __init__(self):
        super().__init__()
        self.DISCORD_LINK = 'https://discord.com/api/webhooks/1045437993525190717' \
                            '/3Vlj_fKPiuCENNesArlsT5unKgKbP_gBEngaz34Fq7kn41NOI00UryowBodqZy2OjZoJ'
        self.LOG_GROUP = '/aws/elasticbeanstalk/Torium-api/var/log/nginx/access.log'
        self.TITLE = "**ACCESS ERROR**"
