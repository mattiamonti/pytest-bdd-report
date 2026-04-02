from typing import Self, override

from pytest_bdd_report.entities.step import Step
from pytest_bdd_report.extensions.step_information import (
    step_information_repo,
)
from pytest_bdd_report.templates.template import BaseTemplate


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
        text_information, json_information = self._embed_text_information(data)
        return self.template.render(
            keyword=data.keyword,
            name=data.name,
            status=data.status.value,
            duration=data.duration,
            text_information=text_information,
            json_information=json_information,
        )

    @staticmethod
    def _embed_text_information(data: Step) -> tuple[str | None, str | None]:
        step_information = step_information_repo.get(data.keyword, data.name)
        if step_information is None:
            return None, None
        return step_information.text, step_information.json
