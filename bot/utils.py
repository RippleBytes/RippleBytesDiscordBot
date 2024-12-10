import requests


DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1315594506879631450/AU_p63eAL9PEBwhmbss1x27MhNJgSkQbmHjzbXUJNw-TvEBxZ5oPq6yJzBVg4LcP7CK_'  
def send_discord_message(message):
    data = message
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)

    if response.status_code == 204:
        print("Message sent to Discord successfully.")
    else:
        print(f"Failed to send message to Discord: {response.status_code}")