import datetime
from typing import override, Self

from pytest_bdd_report.templates.template import BaseTemplate


class ReportTemplate(BaseTemplate):
    def __init__(self) -> None:
        self.rendered_summary: str = ""
        self.rendered_features: str = ""
        self.rendered_feature_statistics: str = ""
        self.test_file_uri: list[str] = []
        self.path: str = "report.html"
        self.file_path: str = ""
        super().__init__(self.path)

    @override
    def render_template(self, data: str, already_rendered_data: str = "") -> str:
        """
        Render the report template.
        """
        return self.template.render(
            title=data.replace(".html", ""),
            date_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            test_file_uri=self.test_file_uri,
            file_path=self.file_path,
            summary=self.rendered_summary,
            features=self.rendered_features,
            feature_statistics=self.rendered_feature_statistics,
        )


class ReportTemplateBuilder:
    def __init__(self) -> None:
        self.report_template: ReportTemplate = ReportTemplate()

    def add_rendered_summary(self, rendered_summary: str) -> Self:
        """
        Add rendered summary to inject into the template.
        """
        self.report_template.rendered_summary = rendered_summary
        return self

    def add_rendered_features(self, rendered_features: str) -> Self:
        """
        Add rendered features to inject into the template.
        """
        self.report_template.rendered_features = rendered_features
        return self

    def add_rendered_feature_statistics(self, rendered_feature_statistics: str) -> Self:
        """
        Add rendered feature statistics to inject into the template.
        """
        self.report_template.rendered_feature_statistics = rendered_feature_statistics
        return self

    def add_test_file_uri(self, test_file_uri: list[str]) -> Self:
        """
        Add test file URIs to the template.
        """
        self.report_template.test_file_uri = test_file_uri
        return self

    def add_file_path(self, file_path: str) -> Self:
        """
        Add file path to the template.
        """
        self.report_template.file_path = file_path
        return self

    def build(self) -> ReportTemplate:
        return self.report_template
