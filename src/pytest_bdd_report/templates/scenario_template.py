import re

from pytest_bdd_report.components.scenario import Scenario
from pytest_bdd_report.templates.template import BaseTemplate


class ScenarioTemplate(BaseTemplate):
    def __init__(self) -> None:
        self.path = "scenario.html"
        super().__init__(self.path)

    def render_template(self, data: Scenario, rendered_steps: str = "") -> str:
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
    def _format_tags(tags: list[dict]):
        if tags is None or tags == []:
            return ""
        result = ""
        for tag in tags:
            result += f"{tag['name']}, "
        return result

    @staticmethod
    def _check_for_parameters(id: str):
        match = re.search(r"\[(.*?)]", id)
        if match:
            res = match.group(1)
            return res.replace("-", ", ")
        else:
            return ""
