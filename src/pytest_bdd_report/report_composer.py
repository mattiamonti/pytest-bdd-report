from typing import Protocol
from pytest_bdd_report.components.feature import Feature
from pytest_bdd_report.extractor import FeatureExtractor
from pytest_bdd_report.loader import ILoader


class IReport(Protocol):
    features: list[Feature]


class ReportComposer:
    def __init__(self, loader: ILoader, report: IReport) -> None:
        self.data: list[dict] = loader.load()
        self.report = report

    def create_report(self):
        features = FeatureExtractor().extract_from(self.data)
        self.report.features = features
        self._calculate_durations()
        return self.report

    def _calculate_durations(self) -> None:
        for feature in self.report.features:
            for scenario in feature.scenarios:
                scenario.calculate_duration()
            feature.calculate_duration()
