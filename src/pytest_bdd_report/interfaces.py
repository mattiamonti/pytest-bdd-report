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
    path: str  # For type checking, indicating implementing classes should have this attribute

    def load(self) -> list[dict]:
        ...


class IReportBuilder(Protocol):
    def set_features(self, features: list):
        ...

    def build(self) -> IReport:
        """
        Build the report, this should be used at the end of the building function chain.
        @return: report object
        """
        ...
