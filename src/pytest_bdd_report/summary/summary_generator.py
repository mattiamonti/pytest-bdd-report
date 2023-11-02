from pytest_bdd_report.interfaces import IReport
from pytest_bdd_report.summary.summary import Summary
from pytest_bdd_report.report import Report


class SummaryGenerator:
    def __init__(self):
        self.summary = Summary()

    def populate_summary(self, report: IReport) -> Summary:
        """
        Populate the summary based on the report provided.
        @param report: from which create the summary
        @return: summary object
        """
        self._set_report_title(report)
        self._get_test_statistics(report)
        self._get_top_feature_fail(report)
        self._calculate_percentage_test_passed()
        self._get_total_duration(report)
        return self.summary

    def _set_report_title(self, report: IReport) -> None:
        """
        Set the summary title as the report title.
        @param report:
        @return:
        """
        self.summary.report_title = report.title

    def _get_test_statistics(self, report: IReport) -> None:
        """
        Calculate the test session statistics based on the report provided.
        @param report:
        @return:
        """
        for feature in report.features:
            self.summary.total_test += feature.total_tests
            self.summary.test_passed += feature.passed_tests
            self.summary.test_failed += feature.failed_tests
            self.summary.test_skipped += feature.skipped_tests

    def _get_top_feature_fail(self, report: IReport) -> None:
        failed_features = filter(lambda x: x.failed_tests > 0, report.features)
        sorted_features = sorted(
            failed_features, key=lambda x: x.failed_tests, reverse=True
        )
        self.summary.top_feature_fail = sorted_features[:5]

    def _get_start_time(self) -> None:
        # TODO implement
        ...

    def _get_total_duration(self, report: IReport) -> None:
        """
        Calculate the total duration of the test session based on the report provided.
        @param report:
        @return:
        """
        duration = 0.0
        for feature in report.features:
            duration += feature.duration
        self.summary.total_duration = duration

    def _calculate_percentage_test_passed(self) -> None:
        """
        Calculate the percentage of the test passed based on the total number of tests.
        @return:
        """
        if self.summary.total_test != 0:
            self.summary.percentage_test_passed = int(
                round(self.summary.test_passed / self.summary.total_test * 100, 0)
            )
