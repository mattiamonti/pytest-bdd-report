from pytest_bdd_report.components.feature import Feature
from pytest_bdd_report.templates.template import BaseTemplate
from typing import List, Dict


class FeatureTemplate(BaseTemplate):
    def __init__(self) -> None:
        self.path = "feature.html"
        super().__init__(self.path)

    def render_template(self, data: Feature, rendered_scenarios: str = "") -> str:
        failed_scenarios_names = [
            scenario.name for scenario in data.scenarios if scenario.status == "failed"
        ]
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
            failed_scenarios_names=failed_scenarios_names,
        )

    @staticmethod
    def _format_tags(tags: List[Dict[str, str]]) -> str:
        """
        Format tags into a comma-separated string.
        """
        if not tags:
            return ""
        return ", ".join(tag["name"] for tag in tags)
