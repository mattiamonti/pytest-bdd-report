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
        )
