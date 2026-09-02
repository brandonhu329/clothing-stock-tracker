import requests


def send_notification():
    topic = "YOUR_TOPIC_HERE"

    message = "Hollister M Regular is back in stock!"

    requests.post(
        f"https://ntfy.sh/{topic}",
        data=message
    )
    