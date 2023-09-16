from pytest_bdd_report.components.step import Step
from pytest_bdd_report.templates.template import BaseTemplate


class StepTemplate(BaseTemplate):
    def __init__(self, step: Step) -> None:
        self.path = "step.html"
        self.step = step

    def render_template(self) -> str:
        self.template.render()
        self.step
        ...
