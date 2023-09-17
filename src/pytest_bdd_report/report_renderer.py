from pytest_bdd_report.components.scenario import Scenario
from pytest_bdd_report.components.step import Step
from pytest_bdd_report.report import Report
from pytest_bdd_report.templates.feature_template import FeatureTemplate
from pytest_bdd_report.templates.scenario_template import ScenarioTemplate
from pytest_bdd_report.templates.step_template import StepTemplate
from pytest_bdd_report.templates.summary_template import SummaryTemplate


class ReportFileGenerator:
    def __init__(self) -> None:
        self.report_content = ""
        pass

    def create_report_file(self, report: Report, path: str) -> None:
        """
        Create the report in the provided file path.
        """
        data = self._render_features(report)
        self.report_content = self._render_summary(data)
        self._save_report_to_file(path)

        ...

    def _render_summary(self, data: str) -> str:
        """
        Render the summary and append it on the report content
        """
        summary_template = SummaryTemplate()
        return summary_template.render_template(data)

    def _render_features(self, report: Report) -> str:
        """
        Render the features and append it on the report content
        """
        feature_template = FeatureTemplate()
        rendered_features = ""
        for feature in report.features:
            rendered_scenarios = self._render_scenarios(feature.scenarios)
            rendered_features += feature_template.render_template(
                feature, rendered_scenarios
            )

        return rendered_features

    def _render_scenarios(self, scenarios: list[Scenario]) -> str:
        template = ScenarioTemplate()
        rendered_scenarios = ""
        for scenario in scenarios:
            rendered_steps = self._render_steps(scenario.steps)
            rendered_scenarios += template.render_template(scenario, rendered_steps)

        return rendered_scenarios

    def _render_steps(self, steps: list[Step]) -> str:
        template = StepTemplate()  # TODO spostare la creazione della classe
        # (che si occupa di caricare il template) in un posto dove non venga chiamata nei loop
        rendered_steps = ""
        for step in steps:
            rendered_steps += template.render_template(step)
        return rendered_steps

    def _save_report_to_file(self, path: str) -> None:
        with open(path, "w") as f:
            f.write(self.report_content)
