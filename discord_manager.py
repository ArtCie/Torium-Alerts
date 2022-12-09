import json

import urllib3


class DiscordManager:
    @staticmethod
    def prepare_discord_message(title, description, color=14177041):
        return {
            "embeds": [
                {
                    "title": title,
                    "description": description,
                    "color": color
                }
            ]
        }

    def send_discord_messages(self, errors, link):
        for error in errors:
            self.send_message(error, link)

    @staticmethod
    def send_message(message, link):
        http = urllib3.PoolManager()
        r = http.request(
            "POST", link,
            body=json.dumps(message),
            headers={'Content-Type': 'application/json'})
        return r.data