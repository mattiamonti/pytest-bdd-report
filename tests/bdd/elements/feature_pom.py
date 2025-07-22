from playwright.sync_api import Page, Locator, expect
import pytest


class FeaturePOM:
    def __init__(self, page: Page, name: str = None) -> None:
        self.page = page
        self.name = name

    def get(self, feature_name: str = None) -> Locator:
        if feature_name is None:
            feature_name = self.name
        return self.page.locator(f"//div[@id='{feature_name}']")

    def should_be_visible(self, feature_name: str = None) -> None:
        if feature_name is None:
            feature_name = self.name
        expect(self.get(feature_name)).to_be_visible()
        expect(self.get(feature_name)).to_be_in_viewport()

    def should_not_be_visible(self, feature_name: str = None) -> None:
        if feature_name is None:
            feature_name = self.name
        expect(self.get(feature_name)).not_to_be_visible()

    def get_all(self) -> list[Locator]: #FIXME move this in a new class ReportPOM, not in the scope of this class
        return self.page.locator(".feature")

    def should_have_description(self, description: str, feature_name: str = None) -> None:
        if feature_name is None:
            feature_name = self.name
        expect(self.get(feature_name)).to_contain_text(description)

    def should_have_path(self, path: str, feature_name: str = None) -> None:
        if feature_name is None:
            feature_name = self.name
        expect(self.get(feature_name)).to_contain_text(path)

    def get_duration(self, feature_name: str = None) -> float:
        if feature_name is not None:
            feature = self.get(feature_name)
        else:
            feature = self.get()

        duration = feature.get_by_text("Executed in").all_inner_texts()
        duration = duration[0].replace("Executed in ", "").replace("ms", "").replace("m", "")
        duration_number = float(duration)
        return duration_number

    def get_scenario_badge(self, scenario_type: str) -> int:
        assert scenario_type in ["passed", "failed", "skipped"], f"Scenario type {scenario_type} not correct, try: passed, failed or skipped"
        feature = self.get()
        badge = feature.get_by_title(f"Number of test {scenario_type}").all_inner_texts()
        return int(badge[0].strip())
