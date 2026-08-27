from playwright.sync_api import sync_playwright

url = "https://www.hollisterco.com/shop/us/p/relaxed-everyday-tee-62788823?seq=33"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()
    page.goto(url)

    print(page.title())

    wanted_size = "M"

    input_id = f"pdp_radio_size_primary_{wanted_size}"

    size_label = page.locator(f'label[for="{input_id}"]')

    print("Trying to select size:", wanted_size)

    size_label.click()

    print("Selected size:", wanted_size)

    page.wait_for_timeout(1000)

    add_button = page.get_by_role("button", name="Add To Bag").first

    if add_button.is_enabled():
        print(wanted_size, "IS IN STOCK")
    else:
        print(wanted_size, "IS OUT OF STOCK")

    input("Press Enter to close the browser...")

    browser.close()