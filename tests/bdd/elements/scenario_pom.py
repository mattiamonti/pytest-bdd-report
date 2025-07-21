from playwright.sync_api import Page, Locator, expect
import pytest

class ScenarioPOM:
    def __init__(self, page: Page) -> None:
        self.page = page

    def get(self, name: str) -> Locator:
        return self.page.locator(f"//*[@id='{name}']/div")

    def scroll_to(self, name: str) -> None:
        scenario = self.get(name)
        scenario.scroll_into_view_if_needed()

    def should_be_visible(self, name: str) -> None:
        expect(self.get(name)).to_be_in_viewport()

    def is_passed(self, name: str) -> None:
        expect(self.get(name)).to_contain_class("scenario-passed")

    def is_failed(self, name: str) -> None:
        expect(self.get(name)).to_contain_class("scenario-failed")

    def is_skipped(self, name: str) -> None:
        expect(self.get(name)).to_contain_class("scenario-skipped")

    def get_all(self) -> list[Locator]:
        return self.page.locator(".scenario")

    def get_passed(self) -> list[Locator]:
        return self.page.locator(".scenario-passed")

    def get_failed(self) -> list[Locator]:
        return self.page.locator(".scenario-failed")

    def get_skipped(self) -> list[Locator]:
        return self.page.locator(".scenario-skipped")