from playwright.sync_api import sync_playwright


BOOKIECO_URL = "https://agents.bookieco.com.cy/"


def search_bookieco(match_text="Olympiacos"):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            executable_path="/usr/bin/chromium",
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        page = browser.new_page(
            viewport={
                "width": 1440,
                "height": 1200
            }
        )

        page.goto(
            BOOKIECO_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        # Give the betting application time to load
        page.wait_for_timeout(15000)

        # Get visible text
        body_text = page.locator("body").inner_text()

        # If normal text is empty, also inspect the HTML
        if not body_text.strip():

            html = page.content()

            return (
                "PAGE TEXT WAS EMPTY\n\n"
                "PAGE TITLE:\n"
                + page.title()
                + "\n\nURL:\n"
                + page.url
                + "\n\nHTML PREVIEW:\n"
                + html[:10000]
            )

        return body_text
