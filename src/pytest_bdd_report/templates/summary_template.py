from pytest_bdd_report.summary.summary import Summary
from pytest_bdd_report.templates.template import BaseTemplate


class SummaryTemplate(BaseTemplate):
    def __init__(self) -> None:
        self.path = "summary.html"
        super().__init__(self.path)

    def render_template(self, data: Summary, **kwargs) -> str:
        return self.template.render(
            total=data.total_test,
            passed=data.test_passed,
            failed=data.test_failed,
            skipped=data.test_skipped,
            percentage=data.percentage_test_passed,
            duration=round(data.total_duration, 5),
            top_feature_fail=data.top_feature_fail,
        )
