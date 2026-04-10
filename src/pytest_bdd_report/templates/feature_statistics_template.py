from typing import override, Self
from pytest_bdd_report.entities.feature import Feature
from pytest_bdd_report.templates.template import BaseTemplate


class FeatureStatisticsTemplate(BaseTemplate):
    _instance: Self | None = None

    def __new__(cls: type[Self], *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # Guard against re-initialization when singleton is reused
        if getattr(self, "_initialized", False):
            return
        self.path: str = "feature_statistics.html"
        super().__init__(self.path)
        self._initialized = True

    @override
    def render_template(self, data: Feature, already_rendered_data: str = "") -> str:
        passed_rate = self._calculate_passed_rate(data)
        return self.template.render(
            name=data.name,
            total=data.total_tests,
            passed=data.passed_tests,
            failed=data.failed_tests,
            skipped=data.skipped_tests,
            duration=round(data.duration, 5),
            rate=passed_rate,
        )

    def _calculate_passed_rate(self, data: Feature) -> int:
        """
        Calculate the passed rate percentage.
        """
        if data.total_tests == 0:
            return 0
        return int(round(data.passed_tests / data.total_tests * 100))
