from jinja2 import Environment, FileSystemLoader


class BaseTemplate:
    def __init__(self) -> None:
        self.path = ""
        self.template = self._load_template(self.path)

    def _load_template(self, path: str):
        environment = Environment(loader=FileSystemLoader("html_templates/"))
        return environment.get_template(self.path)

    def render_template(self) -> str:
        ...
