from pytest_bdd_report.components.scenario import Scenario
from dataclasses import dataclass


@dataclass
class Feature:
    def __init__(
        self,
        id: str,
        name: str,
        line: int,
        description: str,
        tags: list,
        uri: str,
        scenarios: list[Scenario],
        duration: float = 0.0,
        status: str = "passed",
    ):
        self.id = id
        self.name = name
        self.line = line
        self.description = description
        self.tags = tags
        self.uri = uri
        self.scenarios = scenarios
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.skipped_tests = 0
        self.duration = duration
        self.status = status

    def calculate_duration(self) -> None:
        duration = 0
        for scenario in self.scenarios:
            duration += scenario.duration
        self.duration = duration

    def add_scenario(self, scenario: Scenario) -> None:
        self.scenarios.append(scenario)

    def set_total_tests(self, quantity: int):
        self.total_tests = quantity

    def set_failed_tests(self, quantity: int):
        self.failed_tests = quantity

    def set_passed_tests(self, quantity: int):
        self.passed_tests = quantity

    def set_skipped_test(self, quantity: int):
        self.skipped_tests = quantity
