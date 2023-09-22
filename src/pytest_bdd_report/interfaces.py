from abc import ABC, abstractmethod
from typing import Protocol
from pytest_bdd_report.components.feature import Feature


class IReport(Protocol):
    title: str
    features: list[Feature]


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
