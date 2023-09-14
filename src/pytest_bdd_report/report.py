from dataclasses import dataclass
from pytest_bdd_report.components.feature import Feature

@dataclass
class Report:
    title: str
    features: list[Feature]

    def add_feature(self, feature: Feature) -> None:
        self.features.append(feature)