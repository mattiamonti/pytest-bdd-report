from pytest_bdd_report.interfaces import IReport, ISummary
from pytest_bdd_report.renderer import FeatureRenderer, FeatureStatisticsRenderer
from pytest_bdd_report.summary.summary import Summary
from pytest_bdd_report.templates.feature_statistics_template import (
    FeatureStatisticsTemplate,
)
from pytest_bdd_report.templates.feature_template import FeatureTemplate
from pytest_bdd_report.templates.report_template import ReportTemplate
from pytest_bdd_report.templates.summary_template import SummaryTemplate


class ReportFileGenerator:
    def __init__(self) -> None:
        self.report_content = ""

    def create_report_file(self, report: IReport, summary: ISummary, path: str) -> None:
        """
        Create the report in the provided file path.
        """
        rendered_features = self._render_features(report)
        rendered_summary = self._render_summary(summary)
        rendered_feature_statistics = self._render_feature_statistics(report)
        self.report_content = self._render_report(
            report.title,
            rendered_summary,
            rendered_features,
            rendered_feature_statistics,
        )
        self._save_report_to_file(path)

    @staticmethod
    def _render_features(report: IReport) -> str:
        """
        Render the features and return them as a string.
        """
        feature_renderer = FeatureRenderer()
        return feature_renderer.render(report.features, FeatureTemplate())

    @staticmethod
    def _render_summary(data: ISummary) -> str:
        """
        Render the summary and return it as a string.
        """
        summary_template = SummaryTemplate()
        return summary_template.render_template(data)

    @staticmethod
    def _render_feature_statistics(report: IReport) -> str:
        feature_statistics_renderer = FeatureStatisticsRenderer()
        return feature_statistics_renderer.render(
            report.features, FeatureStatisticsTemplate()
        )

    @staticmethod
    def _render_report(
        title: str,
        rendered_summary: str,
        rendered_features: str,
        rendered_feature_statistics: str,
    ) -> str:
        report_template = ReportTemplate()
        report_template.add_rendered_summary(rendered_summary)
        report_template.add_rendered_features(rendered_features)
        report_template.add_rendered_feature_statistics(rendered_feature_statistics)
        return report_template.render_template(title)

    def _save_report_to_file(self, path: str) -> None:
        """
        Save the report content to a file.
        """
        with open(path, "w") as f:
            f.write(self.report_content)
