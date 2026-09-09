from playwright.sync_api import sync_playwright


BOOKIECO_URL = "https://agents.bookieco.com.cy/"


def search_bookieco(match_text="Olympiacos"):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(
            BOOKIECO_URL,
            wait_until="networkidle",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        text = page.locator("body").inner_text()

        browser.close()

        return text
