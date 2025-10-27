import os.path
from typing import Self
from pytest_bdd_report.interfaces import IReport, ISummary
from pytest_bdd_report.renderer import FeatureRenderer, FeatureStatisticsRenderer
from pytest_bdd_report.summary.summary import Summary
from pytest_bdd_report.templates.feature_statistics_template import (
    FeatureStatisticsTemplate,
)
from pytest_bdd_report.templates.feature_template import FeatureTemplate
from pytest_bdd_report.templates.report_template import (
    ReportTemplate,
    ReportTemplateBuilder,
)
from pytest_bdd_report.templates.summary_template import SummaryTemplate


class ReportFile:
    def __init__(self) -> None:
        self.report_content = ""
        self.report_title = ""
        self.rendered_summary = ""
        self.rendered_features = ""
        self.rendered_feature_statistics = ""
        self.test_file_uri: list[str] = []

    def create(self, path: str) -> None:
        """
        Create the report in the provided file path.
        """
        self.report_content = self._render_report(
            self.report_title,
            self.test_file_uri,
            str(os.path.abspath(path)),
            self.rendered_summary,
            self.rendered_features,
            self.rendered_feature_statistics,
        )
        self._save_report_to_file(path)

    @staticmethod
    def _render_report(
        title: str,
        test_file_uri: list[str],
        file_path: str,
        rendered_summary: str,
        rendered_features: str,
        rendered_feature_statistics: str,
    ) -> str:
        report_template = (
            ReportTemplateBuilder()
            .add_rendered_summary(rendered_summary)
            .add_rendered_features(rendered_features)
            .add_rendered_feature_statistics(rendered_feature_statistics)
            .add_test_file_uri(test_file_uri)
            .add_file_path(file_path)
            .build()
        )
        return report_template.render_template(title)

    def _save_report_to_file(self, path: str) -> None:
        """
        Save the report content to the provided file path.
        If the path not exists it will be created.
        """
        if "/" in path:
            os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(self.report_content)


class ReportFileBuilder:
    def __init__(self) -> None:
        self.report_file = ReportFile()

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
