from abc import ABC, abstractmethod
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template

RESOURCES_PATH = Path(__file__).parent.joinpath("html_templates")
ENVIRONMENT = Environment(loader=FileSystemLoader([RESOURCES_PATH]))


class BaseTemplate(ABC):
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.template: Template = self._load_template()

    def _load_template(self):
        """
        Load the template from the html file.
        @return: template
        """
        return ENVIRONMENT.get_template(self.path)

    @abstractmethod
    def render_template(self, data, already_rendered_data: str = "") -> str:
        """
        Render the template with the data provided.
        @param data: object to render
        @param already_rendered_data: (optional) rendered object to inject as plain html
        @return: rendered object
        """
        ...
