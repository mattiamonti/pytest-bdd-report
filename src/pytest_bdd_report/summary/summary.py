from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Protocol


class ISummary(Protocol):
    total_test: int
    test_passed: int
    test_failed: int
    test_skipped: int


@dataclass
class Summary:
    report_title: str = ""
    total_tests: int = 0
    tests_passed: int = 0
    tests_failed: int = 0
    tests_skipped: int = 0
    percentage_tests_passed: float = 0.0
    start_time: Optional[datetime] = None
    total_duration: float = 0
    top_feature_fail: list = None
