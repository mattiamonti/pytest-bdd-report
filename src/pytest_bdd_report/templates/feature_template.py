from pytest_bdd_report.components.feature import Feature
from pytest_bdd_report.templates.template import BaseTemplate


class FeatureTemplate(BaseTemplate):
    def __init__(self) -> None:
        self.path = "feature.html"
        super().__init__(self.path)

    def render_template(self, data: Feature, rendered_scenarios: str = "") -> str:
        return self.template.render(
            id=data.id,
            name=data.name,
            status=data.status,
            duration=data.duration,
            scenarios=rendered_scenarios,
            total=data.total_tests,
            passed=data.passed_tests,
            failed=data.failed_tests,
            skipped=data.skipped_tests,
            description=data.description,
            tags=self._format_tags(data.tags),
        )

    @staticmethod
    def _format_tags(tags: list[dict]):
        if tags is None or tags == []:
            return ""
        result = ""
        for tag in tags:
            result += f"{tag['name']}, "
        return result
