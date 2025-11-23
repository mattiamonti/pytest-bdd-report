from dataclasses import dataclass
from pytest_bdd_report.entities.status_enum import Status


@dataclass
class Step:
    keyword: str
    name: str
    line: int
    status: Status
    duration: int
    error_message: str = ""
