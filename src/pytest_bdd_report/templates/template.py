from pathlib import Path
from abc import ABC, abstractmethod
from jinja2 import Environment, FileSystemLoader, PackageLoader


class BaseTemplate(ABC):
    def __init__(self, path: str) -> None:
        self.path = path
        self.template = self._load_template()

    def _load_template(self):
        resources_path = Path(__file__).parent.joinpath("html_templates")
        environment = Environment(loader=FileSystemLoader([resources_path]))
        # environment = Environment(loader=PackageLoader("templates", "html_templates"))
        return environment.get_template(self.path)

    @abstractmethod
    def render_template(self, data, already_rendered_data: str = "") -> str:
        ...
