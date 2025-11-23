from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol

from pytest_bdd_report.entities.feature import Feature


class ISummary(Protocol):
    total_tests: int
    tests_passed: int
    tests_failed: int
    tests_skipped: int
    percentage_tests_passed: float
    total_duration: float
    top_feature_fail: list[Feature]


@dataclass
class Summary:
    report_title: str = ""
    total_tests: int = 0
    tests_passed: int = 0
    tests_failed: int = 0
    tests_skipped: int = 0
    percentage_tests_passed: float = 0.0
    start_time: datetime | None = None
    total_duration: float = 0
    top_feature_fail: list[Feature] = field(default_factory=list)
