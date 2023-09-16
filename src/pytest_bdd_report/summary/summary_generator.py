from pytest_bdd_report.summary.summary import Summary
from pytest_bdd_report.report import Report


class SummaryGenerator:
    def __init__(self):
        self.summary = Summary()

    def populate_summary(self, report: Report) -> Summary:
        self._set_report_title(report)
        self._get_test_statistics(report)
        self._get_total_duration(report)
        return self.summary

    def _set_report_title(self, report: Report) -> None:
        self.summary.report_title = report.title

    def _get_test_statistics(self, report: Report) -> None:
        for feature in report.features:
            for scenario in feature.scenarios:
                if scenario.status == "failed":
                    self.summary.test_failed += 1
                elif scenario.status == "passed":
                    self.summary.test_passed += 1
                else:
                    self.summary.test_skipped += 1

                self.summary.total_test += 1

    def _get_start_time(self) -> None:
        ...

    def _get_total_duration(self, report: Report) -> None:
        duration = 0.0
        for feature in report.features:
            duration += feature.duration
        self.summary.total_duration = duration
