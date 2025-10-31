from pytest_bdd_report.entities.scenario import Scenario
from pytest_bdd_report.entities.status_enum import Status
from dataclasses import dataclass


@dataclass
class Feature:
    def __init__(
        self,
        id: str,
        name: str,
        line: int,
        description: str,
        tags: list[dict[str, str]],
        uri: str,
        scenarios: list[Scenario],
        duration: float = 0.0,
        status: Status = Status.PASSED,
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

    def __eq__(self, other):
        if isinstance(other, Feature):
            return (
                self.id == other.id
                and self.name == other.name
                and self.description == other.description
                and self.tags == other.tags
                and self.line == other.line
                and self.uri == other.uri
                and self.duration == other.duration
                and self.status == other.status
                and self.total_tests == other.total_tests
                and self.passed_tests == other.passed_tests
                and self.failed_tests == other.failed_tests
                and self.skipped_tests == other.skipped_tests
                and self.scenarios == other.scenarios
            )
        return False
