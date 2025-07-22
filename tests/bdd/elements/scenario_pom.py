from playwright.sync_api import Page, Locator, expect
import pytest


class ScenarioPOM:
    def __init__(self, page: Page, name: str) -> None:
        self.page = page
        self.name = name
        self._scenario = self.page.locator(f"//*[@id='{self.name}']/div")

    def get(self) -> Locator:
        return self._scenario

    def scroll_to(self) -> None:
        scenario = self.get()
        scenario.scroll_into_view_if_needed()

    def should_be_visible(self) -> None:
        expect(self.get()).to_be_in_viewport()

    def is_passed(self) -> None:
        expect(self.get()).to_contain_class("scenario-passed")

    def is_failed(self) -> None:
        expect(self.get()).to_contain_class("scenario-failed")

    def is_skipped(self) -> None:
        expect(self.get()).to_contain_class("scenario-skipped")
