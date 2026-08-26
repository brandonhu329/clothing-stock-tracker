from playwright.sync_api import sync_playwright

url = "https://www.hollisterco.com/shop/us/p/relaxed-everyday-tee-62788823?seq=33"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()
    page.goto(url)

    print(page.title())

    input("Press Enter to close the browser...")

    browser.close()