class LengthMismatchError(Exception):
    """
    Custom exception for a length mismatch between aggregated scenarios and test results.
    """


class ScenarioAndResultMerger:
    """
    Merge scenarios with their corresponding test results.

    This class provides methods to merge aggregated steps information with the associated
    test results, resulting in complete test case details.
    """

    def __init__(self) -> None:
        pass

    def merge_scenario_and_result(
        self, aggregated_scenarios: dict, tests_results: list
    ) -> list:
        """
        Merge aggregated steps information with test results to create complete test cases.

        Args:
            aggregated_scenarios (dict): A dictionary containing aggregated scenario details.
            tests_results (list): A list of test result dictionaries.

        Returns:
            list: A list of merged test case dictionaries.

        Raises:
            LengthMismatchError: If the lengths of aggregated scenarios and test results
            do not match.
        """
        if len(aggregated_scenarios) != len(tests_results):
            raise LengthMismatchError(
                "Lengths of aggregated scenarios and test results do not match."
            )

        merged_results = []

        for details, test_res in zip(aggregated_scenarios.values(), tests_results):
            merged_test_case = self._merge_information(details, test_res)
            merged_results.append(merged_test_case)

        return merged_results

    def _merge_information(self, step_details, test_results) -> dict:
        """
        Merge step details with test results to create a complete test case dictionary.

        Args:
            step_details (dict): Details of the scenario steps.
            test_results (dict): Results of the corresponding test case.

        Returns:
            dict: Merged test case dictionary.
        """

        return {
            "nodeid": test_results["nodeid"],
            "feature": step_details["feature"],
            "scenario": step_details["scenario"],
            "duration": test_results["duration"],
            "outcome": test_results["outcome"],
            "longrepr": test_results["longrepr"],
            "steps": step_details["steps"],
        }
