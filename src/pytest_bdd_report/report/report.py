from dataclasses import dataclass
from typing import Protocol, Self
from pytest_bdd_report.entities.feature import Feature


class IReport(Protocol):
    title: str
    features: list[Feature]


class IReportBuilder(Protocol):
    def set_features(self, features: list[Feature]) -> Self: ...

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


class ReportBuilder:
    def __init__(self, title: str):
        self.report: IReport = Report(title, [])

    def set_features(self, features: list[Feature]) -> Self:
        self.report.features = features
        return self

    def build(self) -> IReport:
        return self.report
