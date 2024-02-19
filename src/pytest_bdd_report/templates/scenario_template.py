import re
from pytest_bdd_report.components.scenario import Scenario
from pytest_bdd_report.templates.template import BaseTemplate
from typing import List, Dict


class ScenarioTemplate(BaseTemplate):
    def __init__(self) -> None:
        self.path: str = "scenario.html"
        super().__init__(self.path)

    def render_template(self, data: Scenario, rendered_steps: str = "") -> str:
        """
        Render the scenario template.
        """
        return self.template.render(
            id=data.id,
            name=data.name,
            status=data.status,
            duration=data.duration,
            steps=rendered_steps,
            error_message=data.error_message,
            description=data.description,
            tags=self._format_tags(data.tags),
            parameters=self._check_for_parameters(data.id),
        )

    @staticmethod
    def _format_tags(tags: List[Dict[str, str]]) -> str:
        """
        Format tags into a comma-separated string.
        """
        return ", ".join(tag["name"] for tag in tags)

    @staticmethod
    def _check_for_parameters(id: str) -> str:
        """
        Check for parameters in the scenario ID and format them.
        """
        match = re.search(r"\[(.*?)]", id)
        if match:
            return match.group(1).replace("-", ", ")
        return ""
