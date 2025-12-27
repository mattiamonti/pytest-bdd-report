from typing import override

from pytest_bdd_report.summary.summary import ISummary
from pytest_bdd_report.templates.template import BaseTemplate


class SummaryTemplate(BaseTemplate):
    def __init__(self) -> None:
        self.path: str = "summary.html"
        super().__init__(self.path)

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
