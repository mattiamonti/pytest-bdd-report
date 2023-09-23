from abc import ABC, abstractmethod
from typing import Protocol
from pytest_bdd_report.components.feature import Feature


class IReport(Protocol):
    title: str
    features: list[Feature]


class ISummary(Protocol):
    total_test: int
    test_passed: int
    test_failed: int
    test_skipped: int


class ILoader(Protocol):
    def __init__(self, path: str):
        self.path = path

    def load(self) -> list[dict]:
        ...


class IReportBuilder(Protocol):
    def set_features(self, features: list):
        ...

    def build(self) -> IReport:
        ...
