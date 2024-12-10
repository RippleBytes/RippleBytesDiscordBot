import requests
from django.conf import settings


def send_discord_message(message):
    data = message
    response = requests.post(settings.DISCORD_WEBHOOK_URL, json=data)

    if response.status_code == 204:
        print("Message sent to Discord successfully.")
    else:
        print(f"Failed to send message to Discord: {response.status_code}")