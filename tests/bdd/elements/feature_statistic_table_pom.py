from playwright.sync_api import Page, Locator, expect
import pytest
from tests.bdd.utils.duration import _extract_duration_from_string


class FeatureStatisticTablePOM:
    def __init__(self, page: Page) -> None:
        self.table = page.get_by_role("table")
        self.row = None
        self._feature_link = "//td[1]"
        self._total = "//td[2]"
        self._passed = "//td[3]"
        self._failed = "//td[4]"
        self._skipped = "//td[5]"
        self._success_rate = "//td[6]"
        self._duration = "//td[7]"

    def get_row(self, feature_name: str) -> Locator:
        self.row = self.table.get_by_test_id(f"feature-table-row-for-{feature_name}")
        return self.row

    def get_column(self, column_name: str) -> Locator:
        assert column_name in [
            "Feature",
            "Total",
            "Passed",
            "Failed",
            "Skipped",
            "Success Rate",
            "Duration",
        ]

        match column_name:
            case "Feature":
                return self.row.locator(self._feature_link)
            case "Total":
                return self.row.locator(self._total)
            case "Passed":
                return self.row.locator(self._passed)
            case "Failed":
                return self.row.locator(self._failed)
            case "Skipped":
                return self.row.locator(self._skipped)
            case "Success Rate":
                return self.row.locator(self._success_rate)
            case "Duration":
                return self.row.locator(self._duration)

    def get_column_duration(self) -> float:
        duration = self.get_column("Duration")
        return _extract_duration_from_string(duration.inner_text())
