from pytest_bdd_report.report import Report
from pytest_bdd_report.components.feature import Feature
from pytest_bdd_report.components.scenario import Scenario
from pytest_bdd_report.components.step import Step


class ReportGenerator:
    def __init__(self, data: list[dict], report: Report) -> None:
        self.data = data
        self.report = report

    def create_report(self) -> Report:
        self.extract_features()
        self.calculate_durations()
        return self.report

    def extract_features(self) -> None:
        for item in self.data:
            if item["keyword"] == "Feature":
                feature = Feature(
                    id=item["id"],
                    name=item["name"],
                    uri=item["uri"],
                    line=item["line"],
                    description=item["description"],
                    tags=item["tags"],
                    scenarios=self.extract_scenarios(item["elements"]),
                )
                self.report.add_feature(feature)

    def extract_scenarios(self, scenarios: list[dict]) -> list[Scenario]:
        list_scenario = []
        for scenario in scenarios:
            list_scenario.append(
                Scenario(
                    id=scenario["id"],
                    name=scenario["name"],
                    line=scenario["line"],
                    description=scenario["description"],
                    tags=scenario["tags"],
                    steps=self.extract_steps(scenario["steps"]),
                )
            )
        return list_scenario

    def extract_steps(self, steps: list[dict]) -> list[Step]:
        list_step = []
        for step in steps:
            list_step.append(
                Step(
                    keyword=step["keyword"],
                    name=step["name"],
                    line=step["line"],
                    status=step["result"]["status"],
                    duration=step["result"]["duration"],
                )
            )
        return list_step

    def calculate_durations(self) -> None:
        for feature in self.report.features:
            for scenario in feature.scenarios:
                scenario.calculate_duration()
            feature.calculate_duration()
