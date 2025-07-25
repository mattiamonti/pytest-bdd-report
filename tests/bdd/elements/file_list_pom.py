from playwright.sync_api import Page, Locator, expect
import pytest
from tests.bdd.utils.duration import get_duration


class FileListPOM:
    def __init__(self, page: Page) -> None:
        self.page = page
        self._button = self.page.get_by_role("group").get_by_text("file paths")
        self._file_list = self.page.locator("//details[contains(@id, 'test-file')]/div")

    def click(self) -> None:
        self._button.click(position={"x": 0, "y": 0})

    def should_be_visible(self) -> None:
        expect(self._file_list).to_be_visible()
        expect(self._file_list).not_to_be_hidden()

    def should_be_hidden(self) -> None:
        expect(self._file_list).to_be_hidden()

    def should_contain(self, path: str) -> None:
        expect(self._file_list).to_contain_text(path)
