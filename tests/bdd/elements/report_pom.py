from playwright.sync_api import Page, Locator, expect
import pytest


class ReportPOM:
    def __init__(self, page: Page):
        self.page = page
        self._feature_locator = ".feature"
        self._scenario_locator = ".scenario"

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

