from playwright.sync_api import Page, Locator, expect
import pytest


class ReportPOM:
    def __init__(self, page: Page):
        self.page = page
        self._feature_locator = ".feature"
        self._scenario_locator = ".scenario"
        self._expand_all_scenarios = self.page.locator("//button[@id='expand-all-scenarios']")
        self._collapse_all_scenarios = self.page.locator("//button[@id='collapse-all-scenarios']")

    def get_all_features(self) -> Locator:
        return self.page.locator(self._feature_locator)

    def get_all_scenarios(self) -> Locator:
        return self.page.locator(self._scenario_locator)

    def get_passed_scenarios(self) -> list[Locator]:
        return self.page.locator(".scenario-passed")

    def get_failed_scenarios(self) -> list[Locator]:
        return self.page.locator(".scenario-failed")

    def get_skipped_scenarios(self) -> list[Locator]:
        return self.page.locator(".scenario-skipped")

    def expand_all_scenarios(self) -> None:
        self._expand_all_scenarios.click()
        expect(self._collapse_all_scenarios).to_be_visible()
        expect(self._expand_all_scenarios).not_to_be_visible()

    def collapse_all_scenarios(self) -> None:
        self._collapse_all_scenarios.click()
        expect(self._expand_all_scenarios).to_be_visible()
        expect(self._collapse_all_scenarios).not_to_be_visible()
