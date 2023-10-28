from pytest_bdd_report.components.feature import Feature
from pytest_bdd_report.templates.template import BaseTemplate


class FeatureStatisticsTemplate(BaseTemplate):
    def __init__(self) -> None:
        self.path = "feature_statistics.html"
        super().__init__(self.path)

    def render_template(self, data: Feature, already_rendered_data: str = "") -> str:
        passed_rate = int(round(data.passed_tests / data.total_tests * 100, 0))
        return self.template.render(
            name=data.name,
            total=data.total_tests,
            passed=data.passed_tests,
            failed=data.failed_tests,
            skipped=data.skipped_tests,
            duration=round(data.duration, 5),
            rate=passed_rate,
        )
