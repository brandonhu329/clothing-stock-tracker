from playwright.sync_api import sync_playwright
import time

url = "https://www.hollisterco.com/shop/us/p/relaxed-everyday-tee-62788823?seq=33"

wanted_size = "M"
wanted_length = "Regular"

check_every = 300  # 300 seconds = 5 minutes


def is_sold_out(label):
    before_content = label.evaluate("""
        (el) => window.getComputedStyle(el, "::before").content
    """)

    return before_content != "none"


def check_stock(page):
    print()
    print("Checking stock...")

    page.goto(url)
    page.wait_for_timeout(1000)

    # Close cookie popup if it appears
    cookie_button = page.get_by_role("button", name="Accept All")

    if cookie_button.count() > 0:
        try:
            cookie_button.first.click(timeout=3000)
            print("Cookie popup closed")
        except:
            pass

    print(page.title())

    # --------------------
    # CHECK SIZE
    # --------------------

    size_input_id = f"pdp_radio_size_primary_{wanted_size}"

    size_input = page.locator(f"#{size_input_id}")
    size_label = page.locator(f'label[for="{size_input_id}"]')

    if size_input.count() == 0:
        print("Could not find size:", wanted_size)
        return False

    if is_sold_out(size_label):
        print(wanted_size, "IS OUT OF STOCK")
        return False

    print(wanted_size, "is available")

    # Select the size
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

    if length_text.count() == 0:
        print("Could not find length:", wanted_length)
        return False

    length_label = length_text.locator(
        "xpath=ancestor::label[1]"
    )

    if length_label.count() == 0:
        print("Could not find length label:", wanted_length)
        return False

    if is_sold_out(length_label):
        print(
            wanted_size,
            wanted_length,
            "IS OUT OF STOCK"
        )
        return False

    print()
    print("*****************************")
    print(
        wanted_size,
        wanted_length,
        "IS IN STOCK!"
    )
    print("*****************************")

    return True


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    while True:
        try:
            in_stock = check_stock(page)

            if in_stock:
                break

            print()
            print("Checking again in 5 minutes...")

            time.sleep(check_every)

        except Exception as error:
            print("Something went wrong:")
            print(error)

            print("Trying again in 5 minutes...")

            time.sleep(check_every)

    browser.close()