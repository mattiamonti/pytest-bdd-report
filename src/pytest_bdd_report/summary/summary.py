from dataclasses import dataclass
from datetime import datetime


@dataclass
class Summary:
    report_title: str = ""
    total_test: int = 0
    test_passed: int = 0
    test_failed: int = 0
    test_skipped: int = 0
    percentage_test_passed: float = 0.0
    start_time: datetime = None
    total_duration: float = 0
    top_feature_fail: list = None
