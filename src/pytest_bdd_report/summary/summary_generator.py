from pytest_bdd_report.summary.summary import Summary
from pytest_bdd_report.report import Report

class SummaryGenerator:
    def __init__(self):
        self.summary = Summary()

    def populate_summary(self, report: Report)-> Summary:
        self._get_test_statistics(report)
        self._get_total_duration(report)
        return self.summary

    def _set_report_title(self) -> None:
        self.summary.report_title = ""

    def _get_test_statistics(self, report: Report) -> None:
        total_test = 0
        test_passed = 0
        test_failed = 0
        test_skipped = 0
        for feature in report.features:
            total_test += len(feature.scenarios)
            for scenario in feature.scenarios:
                if scenario.status == "failed":
                    test_failed += 1
                elif scenario.status == "passed":
                    test_passed += 1
                else:
                    test_skipped +=1

        self.summary.total_test = total_test
        self.summary.test_passed = test_passed
        self.summary.test_failed = test_failed
        self.summary.test_skipped = test_skipped

    def _get_start_time(self) -> None:
        ...

    def _get_total_duration(self, report: Report) -> None:
        duration = 0.0
        for feature in report.features:
            duration += feature.duration
        self.summary.total_duration = duration

            





