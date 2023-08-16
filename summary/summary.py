"""
This module contains the Summary class, which is used to manage and track test summary information.
"""
from utils.json_util import save_to_json


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
