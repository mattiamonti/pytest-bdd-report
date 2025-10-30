from abc import ABC, abstractmethod
from pytest_bdd_report.templates.template import BaseTemplate
from typing import TypeVar, Generic

T = TypeVar("T")


class BaseRenderer(ABC, Generic[T]):
    @abstractmethod
    def render(self, items: list[T], template: BaseTemplate) -> str:
        """
        Render the items into the template.
        @param items: to render
        @param template: in which render the items
        @return: rendered object
        """
        ...
