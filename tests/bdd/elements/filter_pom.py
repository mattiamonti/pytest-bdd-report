from playwright.sync_api import Page, Locator, expect
import pytest


class FilterPOM:
    def __init__(self, page: Page, name: str):
        self.page = page
        assert name in ["passed", "failed", "skipped"]
        self._filter = self.page.locator(f"//label[@for='show-{name}']")
        self._filter_checkbox = self.page.locator(
            f"//input[contains(@id, 'show-{name}')]"
        )

    def get(self) -> Locator:
        return self._filter

    def toggle(self) -> None:
        self.get().click()

    def should_be_enabled(self) -> None:
        expect(self._filter_checkbox).to_be_checked()

    def should_not_be_enabled(self) -> None:
        expect(self._filter_checkbox).not_to_be_checked()
