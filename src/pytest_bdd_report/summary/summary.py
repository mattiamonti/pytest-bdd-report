"""
This module contains the Summary class, which is used to manage and track test summary information.
"""
from pytest_bdd_report.utils.json_util import save_to_json, load_from_json


class Summary:
    """
    Manage and track test summary information.

    This class provides methods to add passed, failed, and skipped tests to the summary,
    as well as save the summary information to a JSON file.
    """

    def __init__(self) -> None:
        self.summary = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "skipped_tests": 0,
        }

    def add_passed_test(self) -> None:
        """
        Add a passed test to the summary.
        """
        self.summary["total_tests"] += 1
        self.summary["passed_tests"] += 1

    def add_failed_test(self) -> None:
        """
        Add a failed test to the summary.
        """
        self.summary["total_tests"] += 1
        self.summary["failed_tests"] += 1

    def add_skipped_test(self) -> None:
        """
        Add a skipped test to the summary.
        """
        self.summary["total_tests"] += 1
        self.summary["skipped_tests"] += 1

    def save_to_json(self, path: str) -> None:
        """
        Save the summary into a JSON file.

        Args:
            path (str): The path to the JSON file.
        """
        save_to_json(self.summary, path)

    def create_feature_statistics(self, path: str):
        """
        Create the statistics for each feature from a JSON file and append it to the summary.

        This function takes a JSON file containing test data and aggregates the
        data to provide statistics on the number of scenarios, tests passed, tests failed,
        tests skipped, scenario durations, and more for each feature.

        Args:
            json_filename (str): The name of the JSON file to be used.
        """
        data = load_from_json(path)

        aggregated_data = {}

        for item in data:
            feature_name = item["feature"]
            scenario_name = item["scenario"]
            scenario_duration = item["duration"]
            test_outcome = item["outcome"]

            if feature_name not in aggregated_data:
                aggregated_data[feature_name] = {
                    "nodeid": item["nodeid"].split("::")[0],
                    "num_scenarios": 1,
                    "num_passed": 1 if test_outcome == "passed" else 0,
                    "num_failed": 1 if test_outcome == "failed" else 0,
                    "num_skipped": 1 if test_outcome == "skipped" else 0,
                    "scenarios": {scenario_name: scenario_duration},
                    "total_duration": scenario_duration,
                }
            else:
                feature_info = aggregated_data[feature_name]
                feature_info["num_scenarios"] += 1
                feature_info["num_passed"] += 1 if test_outcome == "passed" else 0
                feature_info["num_failed"] += 1 if test_outcome == "failed" else 0
                feature_info["num_skipped"] += 1 if test_outcome == "skipped" else 0
                feature_info["scenarios"][scenario_name] = scenario_duration
                feature_info["total_duration"] += scenario_duration

        self.summary["features"] = aggregated_data
