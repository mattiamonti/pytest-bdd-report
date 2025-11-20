import re
from pytest_bdd_report.entities.scenario import Scenario
from pytest_bdd_report.entities.status_enum import Status
from pytest_bdd_report.templates.template import BaseTemplate
from typing import Self, override
from pytest_bdd_report.extensions.screenshot import screenshot_repo


class ScenarioTemplate(BaseTemplate):
    _instance: Self | None = None

    def __new__(cls: type[Self], *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.path: str = "scenario.html"
        super().__init__(self.path)

    @override
    def render_template(self, data: Scenario, already_rendered_data: str = "") -> str:
        """
        Render the scenario template.
        """
        return self.template.render(
            id=data.id,
            name=data.name,
            status=data.status.value,
            duration=data.duration,
            steps=already_rendered_data,
            error_message=data.error_message,
            description=data.description,
            tags=self._format_tags(data.tags),
            parameters=self._check_for_parameters(data.id),
            image_base64=self._embed_screenshot(data),
        )

    @staticmethod
    def _format_tags(tags: list[dict[str, str]]) -> str:
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

    @staticmethod
    def _embed_screenshot(data: Scenario) -> str | None:
        if data.status == Status.FAILED:
            screenshot = screenshot_repo.get(data.feature_name, data.name)
            if screenshot is None:
                return None
            return screenshot.encoded_image
