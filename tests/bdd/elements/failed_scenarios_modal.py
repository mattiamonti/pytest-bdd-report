from playwright.sync_api import Page, Locator, expect
import pytest


class FailedScenariosModalPOM:
    def __init__(self, page: Page) -> None:
        self.page = page # necessary to use the screenshot on fail feature of playwright
        self.modal = page.get_by_role("dialog")
        self.open_button = page.get_by_role("button").get_by_text(
            "failed scenario links"
        )
        self.close_button = self.modal.get_by_role("button")
        self.links = self.modal.get_by_role("link")

    def open(self) -> None:
        self.open_button.scroll_into_view_if_needed()
        expect(self.open_button).to_be_in_viewport()
        self.open_button.click()

    def open_button_should_be_visible(self) -> None:
        self.open_button.scroll_into_view_if_needed()
        expect(self.open_button).to_be_visible()
        expect(self.open_button).to_be_in_viewport()

    def open_button_should_not_be_visible(self) -> None:
        expect(self.open_button).not_to_be_visible()
        expect(self.open_button).not_to_be_in_viewport()

    def close(self) -> None:
        expect(self.close_button).to_be_in_viewport()
        self.close_button.click()

    def should_be_visible(self) -> None:
        expect(self.modal).to_be_visible()

    def should_not_be_visible(self) -> None:
        expect(self.modal).not_to_be_visible()

    def get_links(self) -> Locator:
        return self.links

    def should_contain_link(self, link_name: str):
        expect(self.links.get_by_text(link_name)).to_be_visible()

    def click_on_link(self, link_name: str):
        link = self.links.get_by_text(link_name)
        expect(link).to_be_visible()
        link.click()
