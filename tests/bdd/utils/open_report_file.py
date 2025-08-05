from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import Page
import time
import pytest


def open_report_file_with_retry(page: Page, uri: str, retries: int = 3) -> None:
    report_url = uri
    if "file://" not in report_url:
        report_url = "file://" + uri

    for attempt in range(retries):
        try:
            page.goto(report_url, wait_until="domcontentloaded", timeout=60000)
            break
        except PlaywrightTimeoutError:
            if attempt == retries - 1:
                raise
            time.sleep(5)
