from playwright.sync_api import Page, Locator, expect
import pytest

class ScenarioPOM:
    def __init__(self, page: Page, name: str) -> None:
        self.page = page

    def get(self, name: str) -> Locator:
        return self.page.locator(f"//*[@id='{name}']/div")

    def scroll_to(self, name: str) -> None:
        scenario = self.get(name)
        scenario.scroll_into_view_if_needed()

    def should_be_visible(self, name: str) -> None:
        expect(self.get(name)).to_be_in_viewport()
