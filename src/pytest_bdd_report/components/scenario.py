from typing import List
from dataclasses import dataclass
from pytest_bdd_report.components.step import Step


@dataclass
class Scenario:
    id: str
    name: str
    line: int
    description: str
    tags: List[str]
    steps: List[Step]
    duration: float = 0.0
    status: str = "passed"
    error_message: str = ""

    def calculate_duration(self) -> None:
        self.duration = sum(step.duration for step in self.steps) / 1_000_000_000  # from nanosecond to second

    def add_step(self, step: Step) -> None:
        self.steps.append(step)

    def check_and_add_error_message(self):
        for step in self.steps:
            if step.error_message:
                self.error_message = step.error_message
                break
