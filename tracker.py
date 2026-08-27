from playwright.sync_api import sync_playwright

url = "https://www.hollisterco.com/shop/us/p/relaxed-everyday-tee-62788823?seq=33"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()
    page.goto(url)

    print(page.title())

    sizes = ["XS", "S", "M", "L", "XL", "XXL"]

    for size in sizes:
        input_id = f"pdp_radio_size_primary_{size}"

        size_input = page.locator(f"#{input_id}")

        print("SIZE:", size)
        print(size_input.evaluate("(el) => el.outerHTML"))
        print("DISABLED:", size_input.is_disabled())

    input("Press Enter to close the browser...")

    browser.close()