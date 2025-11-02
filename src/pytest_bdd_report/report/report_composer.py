from typing import Any
from pytest_bdd_report.extractor.extractor import FeatureExtractor
from pytest_bdd_report.entities.feature import Feature
from pytest_bdd_report.report.report import IReport, IReportBuilder
from pytest_bdd_report.loader.json_loader import ILoader


class ReportComposer:
    def __init__(self, loader: ILoader, report_builder: IReportBuilder) -> None:
        self.data: list[dict[str, Any]] = loader.load()
        self.report_builder: IReportBuilder = report_builder
        self.report: IReport | None = None

    def create_report(self) -> IReport:
        """
        Generate the report for the data loaded in the constructor.
        @return: the report
        """
        features = self._extract_features()
        self.report = self.report_builder.set_features(features).build()
        self._calculate_durations()
        return self.report

    def _extract_features(self) -> list[Feature]:
        """
        Extract features from the object data.
        @return: features
        """
        return FeatureExtractor().extract_from(self.data)

    def _calculate_durations(self) -> None:
        """
        Calculate the duration for the scenarios and the features.
        """
        if self.report is not None:
            for feature in self.report.features:
                for scenario in feature.scenarios:
                    scenario.calculate_duration()
                feature.calculate_duration()
