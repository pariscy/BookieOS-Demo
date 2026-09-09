from playwright.sync_api import sync_playwright
import json


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

        captured = []


        # Capture data the website itself receives
        def capture_response(response):

            url = response.url

            if (
                "/api/" in url
                or "/sports/" in url
            ):

                try:

                    text = response.text()

                    if text:
                        captured.append({
                            "url": url,
                            "data": text[:20000]
                        })

                except:
                    pass


        page.on(
            "response",
            capture_response
        )


        page.goto(
            BOOKIECO_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )


        # Let the website run normally
        page.wait_for_timeout(20000)


        body_text = ""

        try:
            body_text = page.locator(
                "body"
            ).inner_text()
        except:
            pass


        result = {
            "page_url": page.url,
            "page_title": page.title(),
            "visible_text": body_text,
            "network_data": captured
        }


        browser.close()


        return json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
