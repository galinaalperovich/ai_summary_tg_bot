import asyncio
import subprocess
from time import sleep

from pyppeteer import launch
from pyppeteer.page import Page
from trafilatura import extract

from summary_bot.settings import (
    FROM_DOCKER,
    HEADERS,
    EXTRA_HTTP_HEADERS,
    WAIT_COND,
    logger,
)


async def extract_article(url: str) -> str:
    """
    Extract the article from the URL with Python's Trafilatura library and Pyppeteer
    """
    # Scrape the page with Pyppeteer headless browser
    scraper = Scraper()
    await scraper.set_browser()
    try:
        page: Page = await scraper.get_response(url)
    except:
        # sometimes the browser crashes, so we need to kill it and start a new one
        await kill_browser_badly(scraper.browser)
        await scraper.set_browser()
        page: Page = await scraper.get_response(url)

    content = await page.content()

    # Extract content from the HTML page
    article = extract(content, favor_recall=True, include_comments=False)

    # Close the page and the browser
    await page.close()
    await scraper.browser.close()
    return article


async def kill_browser_badly(browser):
    browser.pages().close()
    pid = browser.process.pid
    await browser.close()
    subprocess.Popen(f"pkill -f -P {pid}", shell=True)
    subprocess.Popen(f"pkill -f {pid}", shell=True)
    sleep(3)


class Scraper:
    def __init__(self, attempts=1, timeout: int = 25, headless=True):
        self.attempts = attempts
        self.timeout = timeout
        self.headless = headless
        self.browser = None

    async def set_browser(self):
        if self.browser:
            # await kill_browser_badly(self.browser)
            pass
        else:
            logger.info("Setting browser")
            if FROM_DOCKER:
                executable_path = "google-chrome-stable"
            else:
                executable_path = None

            self.browser = await launch(
                executablePath=executable_path,
                **self._get_browser_args(from_docker=FROM_DOCKER),
            )
            logger.info("Setting browser done")

    def _get_browser_args(self, from_docker=False) -> dict:
        args = {
            "headless": self.headless,
            "args": [
                "--lang=en-GB",
                # "--no-zygote",
                # "--ignore-certificate-errors",
                # "--ignore-certificate-errors-spki-list",
                '--user-agent="{}"'.format(HEADERS["User-Agent"]),
            ],
            # "handleSIGINT": False,
            # "handleSIGTERM": False,
            # "handleSIGHUP": False,
            # "ignoreHTTPSErrors": True,
        }
        if from_docker:
            args["args"].extend(
                [
                    "--no-sandbox",
                    "--single-process",
                    "--disable-dev-shm-usage",
                    "--disable-setuid-sandbox",
                ]
            )

        return args

    async def get_response(self, url: str) -> Page:
        logger.info("Check the browser")
        if not self.browser:
            await self.set_browser()
        page: Page = (await self.browser.pages())[0]

        # set http headers
        _ = await asyncio.wait_for(
            page.setExtraHTTPHeaders(EXTRA_HTTP_HEADERS), timeout=self.timeout
        )
        # set user agent
        _ = await asyncio.wait_for(
            asyncio.create_task(page.setUserAgent(HEADERS["User-Agent"])),
            timeout=self.timeout,
        )
        # bring page to front
        _ = await asyncio.wait_for(
            asyncio.create_task(page.bringToFront()), timeout=self.timeout
        )
        # load webpage
        load_task = asyncio.create_task(
            page.goto(url, waitUntil=WAIT_COND, timeout=30000)
        )
        response = await asyncio.wait_for(load_task, timeout=self.timeout)
        status_code = response.status
        if status_code != 200:
            logger.error(f"Received bad status code: {status_code}")
            raise Exception("Bad status code")
        return page
