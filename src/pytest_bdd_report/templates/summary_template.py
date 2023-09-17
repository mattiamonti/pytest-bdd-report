from pytest_bdd_report.templates.template import BaseTemplate


class SummaryTemplate(BaseTemplate):
    def __init__(self) -> None:
        self.path = "summary.html"
        super().__init__(self.path)

    def render_template(self, data: str) -> str:
        return self.template.render(features=data)
