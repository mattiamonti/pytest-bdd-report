from playwright.sync_api import Page, Locator, expect
import pytest


class FeaturePOM:
    def __init__(self, page: Page, name: str) -> None:
        self.page = page
        self.name = name
        self._feature = self.page.locator(f"//div[@id='{self.name}']")

    def get(self) -> Locator:
        return self._feature

    def should_be_visible(self) -> None:
        expect(self.get()).to_be_visible()
        expect(self.get()).to_be_in_viewport()

    def should_not_be_visible(self) -> None:
        expect(self.get()).not_to_be_visible()

    def should_have_description(self, description: str) -> None:
        expect(self.get()).to_contain_text(description)

    def should_have_path(self, path: str) -> None:
        expect(self.get()).to_contain_text(path)

    def get_duration(self) -> float:
        feature = self.get()
        duration = feature.get_by_text("Executed in").all_inner_texts()
        duration = (
            duration[0].replace("Executed in ", "").replace("ms", "").replace("m", "")
        )
        duration_number = float(duration)
        return duration_number

    def get_scenario_badge(self, scenario_type: str) -> int:
        assert scenario_type in [
            "passed",
            "failed",
            "skipped",
        ], f"Scenario type {scenario_type} not correct, try: passed, failed or skipped"
        feature = self.get()
        badge = feature.get_by_title(
            f"Number of test {scenario_type}"
        ).all_inner_texts()
        return int(badge[0].strip())
