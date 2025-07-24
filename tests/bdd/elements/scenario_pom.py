from playwright.sync_api import Page, Locator, expect
import pytest
from tests.bdd.utils.duration import get_duration


class ScenarioPOM:
    def __init__(self, page: Page, name: str) -> None:
        self.page = page
        self.name = name
        self._scenario = self.page.locator(f"//*[@id='{self.name}']/div")
        self._red_background = "rgb(254, 226, 226)"
        self._green_background = "rgb(220, 252, 231)"
        self._yellow_background = "rgb(255, 251, 235)"
        self._error_message_button = self._scenario.get_by_role("group")
        self._error_message = self._error_message_button.locator("//*[contains(@id, 'message')]")

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

    def background_should_be(self, scenario_type: str) -> None:
        assert scenario_type in ["passed", "failed", "skipped"]
        match scenario_type:
            case "passed":
                color = self._green_background
            case "failed":
                color = self._red_background
            case "skipped":
                color = self._yellow_background
        expect(self.get()).to_have_css("background-color", color)

    def toggle_error_message(self) -> None:
        self._error_message_button.click(position={"x": 0, "y": 0})

    def error_message_should_be_hidden(self) -> None:
        expect(self._error_message).to_be_hidden()

    def error_message_should_be_visible(self) -> None:
        expect(self._error_message).not_to_be_hidden()

    def get_duration(self) -> float:
        scenario = self.get()
        return get_duration(scenario)
