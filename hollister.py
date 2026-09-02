from config import URL, WANTED_SIZE, WANTED_LENGTH


def is_sold_out(label):
    before_content = label.evaluate("""
        (el) => window.getComputedStyle(el, "::before").content
    """)

    return before_content != "none"


def check_stock(context):
    page = context.new_page()

    try:
        print()
        print("Checking stock...")

        page.goto(URL)

        page.wait_for_timeout(2000)

        # Close cookie popup
        try:
            cookie_button = page.locator(
                'button:visible',
                has_text="Accept All"
            ).first

            cookie_button.wait_for(
                state="visible",
                timeout=5000
            )

            cookie_button.evaluate(
                "(el) => el.click()"
            )

            page.wait_for_timeout(1000)

            print("Cookie popup closed")

        except Exception:
            print("No cookie popup found")

        print(page.title())

        # --------------------
        # CHECK SIZE
        # --------------------

        size_input_id = f"pdp_radio_size_primary_{WANTED_SIZE}"

        size_input = page.locator(
            f"#{size_input_id}"
        )

        size_label = page.locator(
            f'label[for="{size_input_id}"]'
        )

        if size_input.count() == 0:
            print("Could not find size:", WANTED_SIZE)
            return False

        if is_sold_out(size_label):
            print(WANTED_SIZE, "IS OUT OF STOCK")
            return False

        print(WANTED_SIZE, "is available")

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
            WANTED_LENGTH,
            exact=True
        ).first

        if length_text.count() == 0:
            print("Could not find length:", WANTED_LENGTH)
            return False

        length_label = length_text.locator(
            "xpath=ancestor::label[1]"
        )

        if length_label.count() == 0:
            print(
                "Could not find length label:",
                WANTED_LENGTH
            )
            return False

        if is_sold_out(length_label):
            print(
                WANTED_SIZE,
                WANTED_LENGTH,
                "IS OUT OF STOCK"
            )
            return False

        print()
        print("*****************************")
        print(
            WANTED_SIZE,
            WANTED_LENGTH,
            "IS IN STOCK!"
        )
        print("*****************************")

        return True

    finally:
        page.close()