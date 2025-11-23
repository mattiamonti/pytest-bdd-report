from pytest_bdd_report.entities.step import Step
from pytest_bdd_report.templates.template import BaseTemplate
from typing import override, Self


class StepTemplate(BaseTemplate):
    _instance: Self | None = None

    def __new__(cls: type[Self], *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.path: str = "step.html"
        super().__init__(self.path)

    @override
    def render_template(self, data: Step, already_rendered_data: str = "") -> str:
        return self.template.render(
            keyword=data.keyword,
            name=data.name,
            status=data.status.value,
            duration=data.duration,
        )
