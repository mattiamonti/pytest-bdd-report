from pytest_bdd_report.interfaces import IReport
from pytest_bdd_report.templates.feature_template import FeatureTemplate
from pytest_bdd_report.templates.summary_template import SummaryTemplate
from pytest_bdd_report.renderer import FeatureRenderer


class ReportFileGenerator:
    def __init__(self) -> None:
        self.report_content = ""

    def create_report_file(self, report: IReport, path: str) -> None:
        """
        Create the report in the provided file path.
        """
        rendered_features = self._render_features(report)
        self.report_content = self._render_summary(rendered_features)
        self._save_report_to_file(path)

    @staticmethod
    def _render_features(report: IReport) -> str:
        """
        Render the features and return them as a string.
        """
        feature_renderer = FeatureRenderer()
        return feature_renderer.render(report.features, FeatureTemplate())

    @staticmethod
    def _render_summary(data: str) -> str:
        """
        Render the summary and return it as a string.
        """
        summary_template = SummaryTemplate()
        return summary_template.render_template(data)

    def _save_report_to_file(self, path: str) -> None:
        """
        Save the report content to a file.
        """
        with open(path, "w") as f:
            f.write(self.report_content)
