import os.path
from typing import Self
from pytest_bdd_report.summary.summary import ISummary
from pytest_bdd_report.report.report import IReport
from pytest_bdd_report.renderer.renderer import (
    FeatureRenderer,
    FeatureStatisticsRenderer,
)
from pytest_bdd_report.templates.feature_statistics_template import (
    FeatureStatisticsTemplate,
)
from pytest_bdd_report.templates.feature_template import FeatureTemplate
from pytest_bdd_report.templates.report_template import ReportTemplateBuilder

from pytest_bdd_report.templates.summary_template import SummaryTemplate


class ReportFile:
    def __init__(self) -> None:
        self.report_content: str = ""
        self.report_title: str = ""
        self.rendered_summary: str = ""
        self.rendered_features: str = ""
        self.rendered_feature_statistics: str = ""
        self.test_file_uri: list[str] = []

    def create(self, path: str) -> None:
        """
        Create the report in the provided file path.
        """
        report_template = (
            ReportTemplateBuilder()
            .add_rendered_summary(self.rendered_summary)
            .add_rendered_features(self.rendered_features)
            .add_rendered_feature_statistics(self.rendered_feature_statistics)
            .add_test_file_uri(self.test_file_uri)
            .add_file_path(str(os.path.abspath(path)))
            .build()
        )
        self.report_content = report_template.render_template(self.report_title)
        self._save_report_to_file(path)

    def _save_report_to_file(self, path: str) -> None:
        """
        Save the report content to the provided file path.
        If the path not exists it will be created.
        """
        if "/" in path:
            os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            _ = f.write(self.report_content)


class ReportFileBuilder:
    def __init__(self) -> None:
        self.report_file: ReportFile = ReportFile()

    def add_report(self, report: IReport) -> Self:
        self.report_file.rendered_features = self._render_features(report)
        self.report_file.rendered_feature_statistics = self._render_feature_statistics(
            report
        )
        self.report_file.report_title = report.title
        return self

    def add_summary(self, summary: ISummary) -> Self:
        self.report_file.rendered_summary = self._render_summary(summary)
        return self

    def add_test_file_uri(self, test_file_uri: list[str]) -> Self:
        self.report_file.test_file_uri = test_file_uri
        return self

    def build(self) -> ReportFile:
        return self.report_file

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
