from pytest_bdd_report.components.step import Step
from dataclasses import dataclass


@dataclass
class Scenario:
    id: str
    name: str
    line: int
    description: str
    tags: []
    steps: list[Step]
    duration: float = 0.0
    status: str = "passed"
    error_message: str = ""

    def calculate_duration(self) -> None:
        duration = 0
        for step in self.steps:
            duration += step.duration
        self.duration = duration / 1_000_000_000  # from nanosecond to second

    def add_step(self, step: Step) -> None:
        self.steps.append(step)

    def check_and_add_error_message(self):
        for step in self.steps:
            if step.error_message != "":
                self.error_message = step.error_message
