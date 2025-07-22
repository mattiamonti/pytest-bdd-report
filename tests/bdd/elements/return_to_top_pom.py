from playwright.sync_api import Page, Locator, expect
import pytest

class ReturnToTopPOM:
    def __init__(self, page:Page) -> None:
        self.button = page.get_by_test_id("return-to-top")

    def click(self) -> None:
        self.button.click()

    def hover(self) -> None:
        self.button.hover()

    def should_display_text(self, text: str) -> None:
        expect(self.button.get_by_text(text)).to_be_visible()

    def should_not_display_text(self, text: str) -> None:
        expect(self.button.get_by_text(text)).not_to_be_visible()

