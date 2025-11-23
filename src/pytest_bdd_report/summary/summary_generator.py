from pytest_bdd_report.report.report import IReport
from pytest_bdd_report.summary.summary import Summary


class SummaryGenerator:
    def __init__(self):
        self.summary: Summary = Summary()

    def populate_summary(self, report: IReport) -> Summary:
        """
        Populate the summary based on the report provided.
        @param report: from which create the summary
        @return: summary object
        """
        self._set_report_title(report)
        self._set_test_statistics(report)
        self._set_most_failing_features(report)
        self._set_total_duration(report)
        self._set_percentage_test_passed()
        return self.summary

    def _set_report_title(self, report: IReport) -> None:
        """
        Set the summary title as the report title.
        @param report:
        @return:
        """
        self.summary.report_title = report.title

    def _set_test_statistics(self, report: IReport) -> None:
        """
        Calculate the test session statistics based on the report provided.
        @param report:
        @return:
        """
        for feature in report.features:
            self.summary.total_tests += feature.total_tests
            self.summary.tests_passed += feature.passed_tests
            self.summary.tests_failed += feature.failed_tests
            self.summary.tests_skipped += feature.skipped_tests

    def _set_most_failing_features(self, report: IReport) -> None:
        """
        Get the top 5 features with the highest number of failed tests.
        @param report:
        @return:
        """
        failed_features = [
            feature for feature in report.features if feature.failed_tests > 0
        ]
        sorted_features = sorted(
            failed_features, key=lambda x: x.failed_tests, reverse=True
        )
        self.summary.top_feature_fail = sorted_features[:5]

    def _set_total_duration(self, report: IReport) -> None:
        """
        Calculate the total duration of the test session based on the report provided.
        @param report:
        @return:
        """
        self.summary.total_duration = sum(
            feature.duration for feature in report.features
        )

    def _set_percentage_test_passed(self) -> None:
        """
        Calculate the percentage of the test passed based on the total number of tests.
        @return:
        """
        if self.summary.total_tests != 0:
            try:
                self.summary.percentage_tests_passed = round(
                    self.summary.tests_passed / self.summary.total_tests * 100, 0
                )
            except ZeroDivisionError:
                self.summary.percentage_tests_passed = float("nan")
