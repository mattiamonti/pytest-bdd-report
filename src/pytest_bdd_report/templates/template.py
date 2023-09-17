from jinja2 import Environment, FileSystemLoader


class BaseTemplate:
    def __init__(self, path: str) -> None:
        self.path = path
        self.template = self._load_template()

    def _load_template(self):
        environment = Environment(loader=FileSystemLoader("html_templates/"))
        return environment.get_template(self.path)

    def render_template(self, data) -> str:
        ...
