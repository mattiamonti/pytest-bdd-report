from pytest_bdd_report.components.step import Step
from pytest_bdd_report.templates.template import BaseTemplate


class StepTemplate(BaseTemplate):
    def __init__(self) -> None:
        self.path = "step.html"
        super().__init__(self.path)

    def render_template(self, data: Step, **kwargs) -> str:
        return self.template.render(
            keyword=data.keyword,
            name=data.name,
            status=data.status,
            duration=data.duration,
        )
