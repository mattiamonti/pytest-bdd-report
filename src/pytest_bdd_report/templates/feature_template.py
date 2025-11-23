from pytest_bdd_report.entities.feature import Feature
from pytest_bdd_report.entities.status_enum import Status
from pytest_bdd_report.templates.template import BaseTemplate
from typing import Self, override


class FeatureTemplate(BaseTemplate):
    _instance: Self | None = None

    def __new__(cls: type[Self], *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.path: str = "feature.html"
        super().__init__(self.path)

    @override
    def render_template(self, data: Feature, already_rendered_data: str = "") -> str:
        return self.template.render(
            id=data.id,
            name=data.name,
            status=data.status.value,
            duration=data.duration,
            scenarios=already_rendered_data,
            total=data.total_tests,
            passed=data.passed_tests,
            failed=data.failed_tests,
            skipped=data.skipped_tests,
            description=data.description,
            tags=self._format_tags(data.tags),
            failed_scenarios_names=self._extract_failed_scenarios_name(data),
        )

    @staticmethod
    def _extract_failed_scenarios_name(feature: Feature) -> list[str]:
        """
        @return the names of the failed scenarios in the feature
        """
        failed_scenarios_names = [
            scenario.name
            for scenario in feature.scenarios
            if scenario.status == Status.FAILED
        ]
        return failed_scenarios_names

    @staticmethod
    def _format_tags(tags: list[dict[str, str]]) -> str:
        """
        Format tags into a comma-separated string.
        """
        if not tags:
            return ""
        return ", ".join(tag["name"] for tag in tags)
