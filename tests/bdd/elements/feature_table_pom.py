from playwright.sync_api import Page, Locator, expect
import pytest


class FeatureTablePOM:
    def __init__(self, page: Page) -> None:
        self.page = page

    def get_row(self, feature_name: str) -> Locator:
        row = self.page.get_by_test_id(f"feature-table-row-for-{feature_name}")
        return row

    def click_feature_link(self, feature_name: str) -> None:
        self.get_row(feature_name).get_by_role("link").click()
