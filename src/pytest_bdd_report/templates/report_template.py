from pytest_bdd_report.templates.template import BaseTemplate


class ReportTemplate(BaseTemplate):
    def __init__(self) -> None:
        self.rendered_summary = ""
        self.rendered_features = ""
        self.path = "report.html"
        super().__init__(self.path)

    def render_template(self, data: str, **kwargs) -> str:
        return self.template.render(
            title=data, summary=self.rendered_summary, features=self.rendered_features
        )

    def add_rendered_summary(self, rendered_summary: str):
        self.rendered_summary = rendered_summary

    def add_rendered_features(self, rendered_features: str):
        self.rendered_features = rendered_features
