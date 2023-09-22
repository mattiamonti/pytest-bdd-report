from dataclasses import dataclass
from pytest_bdd_report.components.feature import Feature
from pytest_bdd_report.interfaces import IReportBuilder


@dataclass
class Report:
    title: str
    features: list[Feature]

    def add_feature(self, feature: Feature) -> None:
        self.features.append(feature)


class ReportBuilder(IReportBuilder):
    def __init__(self, title: str):
        self.report = Report(title, [])

    def set_features(self, features: list[Feature]):
        self.report.features = features
        return self

    def build(self) -> Report:
        return self.report
