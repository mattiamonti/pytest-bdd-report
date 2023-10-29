import datetime

from pytest_bdd_report.templates.template import BaseTemplate


class ReportTemplate(BaseTemplate):
    def __init__(self) -> None:
        self.rendered_summary = ""
        self.rendered_features = ""
        self.rendered_feature_statistics = ""
        self.path = "report.html"
        super().__init__(self.path)

    def render_template(self, data: str, **kwargs) -> str:
        return self.template.render(
            title=data,
            date_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            summary=self.rendered_summary,
            features=self.rendered_features,
            feature_statistics=self.rendered_feature_statistics,
        )

    def add_rendered_summary(self, rendered_summary: str) -> None:
        """
        Add rendered summary to inject into the template.
        @param rendered_summary:
        @return:
        """
        self.rendered_summary = rendered_summary

    def add_rendered_features(self, rendered_features: str) -> None:
        """
        Add rendered features to inject into the template.
        @param rendered_features:
        @return:
        """
        self.rendered_features = rendered_features

    def add_rendered_feature_statistics(self, rendered_feature_statistics: str) -> None:
        self.rendered_feature_statistics = rendered_feature_statistics
