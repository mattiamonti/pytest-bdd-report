from dataclasses import dataclass
from typing import Protocol
from pytest_bdd_report.entities.feature import Feature


class IReport(Protocol):
    title: str
    features: list[Feature]


class IReportBuilder(Protocol):
    def set_features(self, features: list): ...

    def build(self) -> IReport:
        """
        Build the report, this should be used at the end of the building function chain.
        @return: report object
        """
        ...


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
