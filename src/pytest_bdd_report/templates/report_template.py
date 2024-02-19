import datetime
from typing import List

from pytest_bdd_report.templates.template import BaseTemplate


class ReportTemplate(BaseTemplate):
    def __init__(self) -> None:
        self.rendered_summary: str = ""
        self.rendered_features: str = ""
        self.rendered_feature_statistics: str = ""
        self.test_file_uri: List[str] = []
        self.path: str = "report.html"
        self.file_path: str = ""
        super().__init__(self.path)

    def render_template(self, data: str, **kwargs) -> str:
        """
        Render the report template.
        """
        return self.template.render(
            title=data,
            date_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            test_file_uri=self.test_file_uri,
            file_path=self.file_path,
            summary=self.rendered_summary,
            features=self.rendered_features,
            feature_statistics=self.rendered_feature_statistics,
        )

    def add_rendered_summary(self, rendered_summary: str) -> None:
        """
        Add rendered summary to inject into the template.
        """
        self.rendered_summary = rendered_summary

    def add_rendered_features(self, rendered_features: str) -> None:
        """
        Add rendered features to inject into the template.
        """
        self.rendered_features = rendered_features

    def add_rendered_feature_statistics(self, rendered_feature_statistics: str) -> None:
        """
        Add rendered feature statistics to inject into the template.
        """
        self.rendered_feature_statistics = rendered_feature_statistics

    def add_test_file_uri(self, test_file_uri: List[str]) -> None:
        """
        Add test file URIs to the template.
        """
        self.test_file_uri = test_file_uri

    def add_file_path(self, file_path: str) -> None:
        """
        Add file path to the template.
        """
        self.file_path = file_path
