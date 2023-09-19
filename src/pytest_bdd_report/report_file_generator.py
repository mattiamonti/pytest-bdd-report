from abc import ABC, abstractmethod
from pytest_bdd_report.report import Report
from pytest_bdd_report.templates.feature_template import FeatureTemplate
from pytest_bdd_report.templates.scenario_template import ScenarioTemplate
from pytest_bdd_report.templates.step_template import StepTemplate
from pytest_bdd_report.templates.summary_template import SummaryTemplate
from pytest_bdd_report.templates.template import BaseTemplate
from pytest_bdd_report.components.step import Step
from pytest_bdd_report.components.scenario import Scenario
from pytest_bdd_report.components.feature import Feature


class ReportFileGenerator:
    def __init__(self) -> None:
        self.report_content = ""
        pass

    def create_report_file(self, report: Report, path: str) -> None:
        """
        Create the report in the provided file path.
        """
        rendered_features = FeatureRenderer().render(report.features, FeatureTemplate())
        self.report_content = self._render_summary(rendered_features)
        self._save_report_to_file(path)

    @staticmethod
    def _render_summary(data: str) -> str:
        """
        Render the summary and append it on the report content
        """
        summary_template = SummaryTemplate()
        return summary_template.render_template(data)

    def _save_report_to_file(self, path: str) -> None:
        with open(path, "w") as f:
            f.write(self.report_content)


class Renderer(ABC):
    @abstractmethod
    def render(self, items: list, template: BaseTemplate) -> str:
        ...


class StepRenderer(Renderer):
    def render(self, items: list[Step], template: StepTemplate) -> str:
        rendered = ""
        for item in items:
            rendered += template.render_template(item)
        return rendered


class ScenarioRenderer(Renderer):
    def render(self, items: list[Scenario], template: ScenarioTemplate) -> str:
        step_renderer = StepRenderer()
        step_template = StepTemplate()
        rendered = ""
        for item in items:
            rendered_steps = step_renderer.render(item.steps, step_template)
            rendered += template.render_template(item, rendered_steps)
        return rendered


class FeatureRenderer(Renderer):
    def render(self, items: list[Feature], template: FeatureTemplate) -> str:
        scenario_renderer = ScenarioRenderer()
        scenario_template = ScenarioTemplate()
        rendered = ""
        for item in items:
            rendered_scenarios = scenario_renderer.render(
                item.scenarios, scenario_template
            )
            rendered += template.render_template(item, rendered_scenarios)
        return rendered
