from playwright.sync_api import sync_playwright

url = "https://www.hollisterco.com/shop/us/p/relaxed-everyday-tee-62788823?seq=33"

wanted_size = "M"
wanted_length = "Regular"


def is_sold_out(label):
    before_content = label.evaluate("""
        (el) => window.getComputedStyle(el, "::before").content
    """)

    return before_content != "none"


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()
    page.goto(url)

    # Close cookie popup
    cookie_button = page.get_by_role("button", name="Accept All")

    if cookie_button.count() > 0:
        cookie_button.first.click()
        print("Cookie popup closed")

    print(page.title())

    # --------------------
    # CHECK SIZE
    # --------------------

    size_input_id = f"pdp_radio_size_primary_{wanted_size}"

    size_input = page.locator(f"#{size_input_id}")
    size_label = page.locator(f'label[for="{size_input_id}"]')

    if size_input.count() == 0:
        print("Could not find size:", wanted_size)

    elif is_sold_out(size_label):
        print(wanted_size, "IS OUT OF STOCK")

    else:
        print(wanted_size, "is available")

        # Select size
        page.evaluate(
            "(id) => document.getElementById(id).click()",
            size_input_id
        )

        page.wait_for_timeout(500)

        # --------------------
        # CHECK LENGTH
        # --------------------

        length_text = page.get_by_text(
            wanted_length,
            exact=True
        ).first

        length_label = length_text.locator(
            "xpath=ancestor::label[1]"
        )

        if length_label.count() == 0:
            print("Could not find length:", wanted_length)

        elif is_sold_out(length_label):
            print(
                wanted_size,
                wanted_length,
                "IS OUT OF STOCK"
            )

        else:
            print(
                wanted_size,
                wanted_length,
                "IS IN STOCK!"
            )

    input("Press Enter to close the browser...")

    browser.close()