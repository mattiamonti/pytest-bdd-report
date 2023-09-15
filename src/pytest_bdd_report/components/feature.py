from pytest_bdd_report.components.scenario import Scenario
from dataclasses import dataclass


@dataclass
class Feature:
    id: str
    name: str
    line: int
    description: str
    tags: list
    uri: str
    scenarios: list[Scenario]
    duration: float = 0.0
    status: str = "passed"

    def calculate_duration(self) -> None:
        duration = 0
        for scenario in self.scenarios:
            duration += scenario.duration
        self.duration = duration

    def add_scenario(self, scenario: Scenario) -> None:
        self.scenarios.append(scenario)
