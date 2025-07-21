
from playwright.sync_api import Page, Locator, expect
import pytest

class FeaturePOM:
    def __init__(self, page: Page) -> None:
        self.page = page

    def get(self, feature_name: str) -> Locator:
        return self.page.locator(f"//div[@id='{feature_name}']")
    
    def should_be_visible(self, feature_name: str) -> None:
        expect(self.get(feature_name)).to_be_visible()
        expect(self.get(feature_name)).to_be_in_viewport()

    def should_not_be_visible(self, feature_name: str) -> None:
        expect(self.get(feature_name)).not_to_be_visible()


