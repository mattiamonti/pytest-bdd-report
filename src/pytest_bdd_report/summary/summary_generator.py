from pytest_bdd_report.interfaces import IReport
from pytest_bdd_report.summary.summary import Summary
from pytest_bdd_report.report import Report


class SummaryGenerator:
    def __init__(self):
        self.summary = Summary()

    def populate_summary(self, report: IReport) -> Summary:
        self._set_report_title(report)
        self._get_test_statistics(report)
        self._get_total_duration(report)
        return self.summary

    def _set_report_title(self, report: IReport) -> None:
        self.summary.report_title = report.title

    def _get_test_statistics(self, report: IReport) -> None:
        for feature in report.features:
            self.summary.total_test += feature.total_tests
            self.summary.test_passed += feature.passed_tests
            self.summary.test_failed += feature.failed_tests
            self.summary.test_skipped += feature.skipped_tests

    def _get_start_time(self) -> None:
        ...

    def _get_total_duration(self, report: IReport) -> None:
        duration = 0.0
        for feature in report.features:
            duration += feature.duration
        self.summary.total_duration = duration
