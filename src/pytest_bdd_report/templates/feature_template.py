from pytest_bdd_report.components.feature import Feature
from pytest_bdd_report.templates.template import BaseTemplate


class FeatureTemplate(BaseTemplate):
    def __init__(self) -> None:
        self.path = "feature.html"
        super().__init__(self.path)

    def render_template(self, data: Feature, rendered_scenarios: str) -> str:
        return self.template.render(
            id=data.id,
            name=data.name,
            status=data.status,
            duration=data.duration,
            scenarios=rendered_scenarios,
        )