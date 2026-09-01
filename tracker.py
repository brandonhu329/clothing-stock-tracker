"""Check whether a specific size of a Hollister product is in stock.

Usage:
    python tracker.py --url "<product url>" --size M
    python tracker.py --url "<product url>" --size M --show-browser

Exit codes:
    0 - size is in stock
    1 - size is out of stock
    2 - could not determine stock (bad URL, size not found, etc.)
"""

import argparse
import sys

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

DEFAULT_URL = "https://www.hollisterco.com/shop/us/p/relaxed-everyday-tee-62788823?seq=33"


def _dismiss_cookie_banner(page) -> None:
    """Accept the OneTrust cookie banner if it's showing.

    It overlays the page and blocks clicks on the size buttons otherwise.
    """
    try:
        page.click("#onetrust-accept-btn-handler", timeout=5000)
    except PlaywrightTimeoutError:
        pass  # banner wasn't shown (e.g. already accepted) - nothing to do


def check_stock(url: str, size: str, headless: bool = True) -> bool:
    """Return True if `size` is in stock for the product at `url`."""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        try:
            page.goto(url)
            _dismiss_cookie_banner(page)

            input_id = f"pdp_radio_size_primary_{size}"
            size_label = page.locator(f'label[for="{input_id}"]')

            if size_label.count() == 0:
                raise ValueError(
                    f"Size '{size}' was not found on this product page."
                )

            size_label.click()
            page.wait_for_timeout(1000)

            add_button = page.get_by_role("button", name="Add To Bag").first
            return add_button.is_enabled()
        finally:
            browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL, help="Product page URL to check.")
    parser.add_argument("--size", required=True, help="Size to check, e.g. S, M, L, XL.")
    parser.add_argument(
        "--show-browser",
        action="store_true",
        help="Show the browser window instead of running headless (useful for debugging).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        in_stock = check_stock(args.url, args.size, headless=not args.show_browser)
    except ValueError as exc:
        print(f"Could not check stock: {exc}")
        return 2

    if in_stock:
        print(f"{args.size} IS IN STOCK")
        return 0
    else:
        print(f"{args.size} IS OUT OF STOCK")
        return 1


if __name__ == "__main__":
    sys.exit(main())
