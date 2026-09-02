from playwright.sync_api import sync_playwright
from hollister import check_stock
from notifications import send_notification
from config import CHECK_EVERY

import time


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context()

    while True:
        try:
            in_stock = check_stock(context)

            if in_stock:
                send_notification()
                break

            print()
            print("Checking again in 5 minutes...")

            time.sleep(CHECK_EVERY)

        except KeyboardInterrupt:
            print()
            print("Tracker stopped")
            break

        except Exception as error:
            print()
            print("Something went wrong:")
            print(error)

            print("Trying again in 5 minutes...")

            time.sleep(CHECK_EVERY)

    browser.close()