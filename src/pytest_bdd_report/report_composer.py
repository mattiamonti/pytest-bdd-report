from pytest_bdd_report.extractor import FeatureExtractor
from pytest_bdd_report.interfaces import IReport, ILoader, IReportBuilder


class ReportComposer:
    def __init__(self, loader: ILoader, report_builder: IReportBuilder) -> None:
        self.data: list[dict] = loader.load()
        self.report_builder = report_builder
        self.report = None

    def create_report(self) -> IReport:
        """
        Generate the report for the data loaded in the constructor.
        @return: the report
        """
        features = self._extract_features()
        self.report_builder.set_features(features)
        self.report = self.report_builder.build()
        self._calculate_durations()
        return self.report

    def _extract_features(self) -> list:
        """
        Extract features from the object data.
        @return: features
        """
        return FeatureExtractor().extract_from(self.data)

    def _calculate_durations(self) -> None:
        """
        Calculate the duration for the scenarios and the features.
        """
        for feature in self.report.features:
            for scenario in feature.scenarios:
                scenario.calculate_duration()
            feature.calculate_duration()
