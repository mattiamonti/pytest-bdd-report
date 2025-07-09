from pytest_bdd_report.summary.summary import Summary
from pytest_bdd_report.templates.template import BaseTemplate


class SummaryTemplate(BaseTemplate):
    def __init__(self) -> None:
        self.path = "summary.html"
        super().__init__(self.path)

    def render_template(self, data: Summary, **kwargs) -> str:
        fail_rate = round(data.tests_failed / data.total_tests * 100, 0)
        return self.template.render(
            total=data.total_tests,
            passed=data.tests_passed,
            failed=data.tests_failed,
            skipped=data.tests_skipped,
            pass_rate=data.percentage_tests_passed,
            fail_rate=fail_rate,
            duration=round(data.total_duration, 5),
            top_feature_fail=data.top_feature_fail,
        )
