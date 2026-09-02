from playwright.sync_api import sync_playwright

from hollister import check_stock
from notifications import send_notification


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context()

    try:
        in_stock = check_stock(context)

        if in_stock:
            send_notification()

    except Exception as error:
        print("Something went wrong:")
        print(error)

    finally:
        browser.close()