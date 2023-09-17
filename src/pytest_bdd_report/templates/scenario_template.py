from pytest_bdd_report.components.scenario import Scenario
from pytest_bdd_report.templates.step_template import StepTemplate
from pytest_bdd_report.templates.template import BaseTemplate


class ScenarioTemplate(BaseTemplate):
    def __init__(self) -> None:
        self.path = "scenario.html"
        super().__init__(self.path)

    def render_template(self, data: Scenario, rendered_steps: str) -> str:
        self.template.render(id=data.id, steps=rendered_steps)

    ...  # TODO implementare
