from playwright.sync_api import sync_playwright

url = "https://www.hollisterco.com/shop/us/p/relaxed-everyday-tee-62788823?seq=33"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()
    page.goto(url)

    print(page.title())

    sizes = ["XS", "S", "M", "L", "XL", "XXL"]

    for size in sizes:
        matches = page.get_by_text(size, exact=True)

        print("SIZE:", size)
        print("FOUND:", matches.count())

        for i in range(matches.count()):
            element = matches.nth(i)
            print(element.evaluate("(el) => el.outerHTML"))

    input("Press Enter to close the browser...")

    browser.close()