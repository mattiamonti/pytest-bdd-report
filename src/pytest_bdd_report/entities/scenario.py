from dataclasses import dataclass
from pytest_bdd_report.entities.step import Step
from pytest_bdd_report.entities.status_enum import Status


@dataclass
class Scenario:
    id: str
    name: str
    line: int
    description: str
    tags: list[dict[str, str]]
    steps: list[Step]
    duration: float = 0.0
    status: Status = Status.PASSED
    error_message: str = ""
    feature_name: str = ""

    def calculate_duration(self) -> None:
        """Calculate the total duration of the scenario in seconds"""
        self.duration = (
            sum(step.duration for step in self.steps) / 1_000_000_000
        )  # from nanosecond to second

    def add_step(self, step: Step) -> None:
        self.steps.append(step)

    def set_feature_name(self, feature_name: str) -> None:
        self.feature_name = feature_name

    def check_and_add_error_message(self):
        for step in self.steps:
            if step.error_message:
                self.error_message = step.error_message
                break
