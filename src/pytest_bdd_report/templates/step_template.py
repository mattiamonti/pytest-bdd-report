from pytest_bdd_report.entities.step import Step
from pytest_bdd_report.templates.template import BaseTemplate
from typing import Optional, Type


class StepTemplate(BaseTemplate):
    _instance: Optional["StepTemplate"] = None

    def __new__(cls: Type["StepTemplate"], *args, **kwargs) -> "StepTemplate":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.path = "step.html"
        super().__init__(self.path)

    def render_template(self, data: Step, **kwargs) -> str:
        return self.template.render(
            keyword=data.keyword,
            name=data.name,
            status=data.status.value,
            duration=data.duration,
        )
