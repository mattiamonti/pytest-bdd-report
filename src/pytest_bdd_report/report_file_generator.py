from pytest_bdd_report.report_composer import IReport
from pytest_bdd_report.templates.feature_template import FeatureTemplate
from pytest_bdd_report.templates.summary_template import SummaryTemplate
from pytest_bdd_report.renderer import FeatureRenderer


class ReportFileGenerator:
    def __init__(self) -> None:
        self.report_content = ""
        pass

    def create_report_file(self, report: IReport, path: str) -> None:
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
