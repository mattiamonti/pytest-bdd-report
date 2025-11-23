from pytest_bdd_report.templates.template import BaseTemplate
from typing import Any, Protocol


class Renderer(Protocol):
    def render(self, items: list[Any], template: BaseTemplate) -> str:
        """
        Render the items into the template.
        @param items: to render
        @param template: in which render the items
        @return: rendered object
        """
        ...
