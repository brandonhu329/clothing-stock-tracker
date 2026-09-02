import os
import requests

from config import WANTED_SIZE, WANTED_LENGTH, URL


def send_notification():
    topic = os.getenv("NTFY_TOPIC")

    if not topic:
        print("Notification topic is not set")
        return

    message = f"Hollister {WANTED_SIZE} {WANTED_LENGTH} is back in stock!"

    response = requests.post(
        f"https://ntfy.sh/{topic}",
        data=message.encode("utf-8"),
        headers={
            "Title": "Hollister Restock",
            "Priority": "5",
            "Click": URL
        }
    )

    if response.ok:
        print("Phone notification sent!")
    else:
        print("Could not send notification")
    