from playwright.sync_api import sync_playwright

url = "https://www.hollisterco.com/shop/us/p/relaxed-everyday-tee-62788823?seq=33"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()
    page.goto(url)

    cookie_button = page.get_by_role("button", name="Accept All")

    if cookie_button.count() > 0:
        cookie_button.first.click()
        print("Cookie popup closed")

    print(page.title())

    wanted_size = "M"

    input_id = f"pdp_radio_size_primary_{wanted_size}"
    size_input = page.locator(f"#{input_id}")

    print("Trying to find size:", wanted_size)
    print("Number of size inputs found:", size_input.count())

    page.evaluate(
    "(id) => document.getElementById(id).click()",
    input_id)

    page.wait_for_timeout(500)

    print("Selected size:", wanted_size)
    print("Checked:", size_input.is_checked())

    input("Press Enter to close the browser...")

    browser.close()