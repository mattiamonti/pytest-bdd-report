from typing import override, Self

from pytest_bdd_report.summary.summary import ISummary
from pytest_bdd_report.templates.template import BaseTemplate


class SummaryTemplate(BaseTemplate):
    _instance: Self | None = None

    def __new__(cls: type[Self], *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # Guard against re-initialization when singleton is reused
        if getattr(self, "_initialized", False):
            return
        self.path: str = "summary.html"
        super().__init__(self.path)
        self._initialized = True

    @override
    def render_template(self, data: ISummary, already_rendered_data: str = "") -> str:
        return self.template.render(
            total=data.total_tests,
            passed=data.tests_passed,
            failed=data.tests_failed,
            skipped=data.tests_skipped,
            pass_rate=data.percentage_tests_passed,
            fail_rate=self._get_fail_rate(data.tests_failed, data.total_tests),
            duration=round(data.total_duration, 5),
            top_feature_fail=data.top_feature_fail,
        )

    @staticmethod
    def _get_fail_rate(failed: int, total: int) -> float:
        try:
            return round(failed / total * 100, 0)
        except ZeroDivisionError:
            return 0
