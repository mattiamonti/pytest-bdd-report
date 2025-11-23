import os
from typing import override, Any

from pytest_bdd_report.entities.feature import Feature
from pytest_bdd_report.entities.scenario import Scenario
from pytest_bdd_report.entities.step import Step
from pytest_bdd_report.entities.status_enum import Status
from pytest_bdd_report.extractor.base_extractor import BaseExtractor


class StepExtractor(BaseExtractor[Step]):
    @override
    def create_item(self, data: dict[str, Any]) -> Step:
        step = Step(
            keyword=data["keyword"],
            name=data["name"],
            line=data["line"],
            status=Status(data["result"]["status"]),
            duration=data["result"]["duration"],
        )
        step.error_message = data["result"].get("error_message", "")
        return step


class ScenarioExtractor(BaseExtractor[Scenario]):
    @override
    def create_item(self, data: dict[str, Any]) -> Scenario:
        steps = StepExtractor().extract_from(data.get("steps", []))
        status = (
            Status.FAILED
            if any(step.status == Status.FAILED for step in steps)
            else Status.PASSED
        )
        scenario = Scenario(
            id=data["id"],
            name=data["name"],
            line=data["line"],
            description=data["description"],
            tags=data["tags"],
            steps=steps,
            status=status,
        )
        scenario.check_and_add_error_message()
        return scenario


class FeatureExtractor(BaseExtractor[Feature]):
    @override
    def create_item(self, data: dict[str, Any]) -> Feature:
        scenarios = ScenarioExtractor().extract_from(data.get("elements", []))
        self._set_feature_name_to_scenarios(data["name"], scenarios)
        failed, passed, total = self._count_failed_passed_total_tests(scenarios)
        status = Status.PASSED if failed == 0 else Status.FAILED
        feature = Feature(
            id=data["id"],
            name=data["name"],
            uri=data["uri"],
            line=data["line"],
            description=data["description"],
            tags=data["tags"],
            scenarios=scenarios,
            status=status,
        )
        skipped = self._check_for_skipped_scenarios(feature)
        feature.set_total_tests(total + skipped)
        feature.set_failed_tests(failed)
        feature.set_passed_tests(passed)
        feature.set_skipped_test(skipped)
        return feature

    @staticmethod
    def _count_failed_passed_total_tests(tests: list[Scenario]) -> tuple[int, int, int]:
        failed = sum(1 for test in tests if test.status == Status.FAILED)
        passed = sum(1 for test in tests if test.status == Status.PASSED)
        total = len(tests)
        return failed, passed, total

    @staticmethod
    def _set_feature_name_to_scenarios(
        feature_name: str, scenarios: list[Scenario]
    ) -> None:
        for scenario in scenarios:
            scenario.set_feature_name(feature_name)

    @staticmethod
    def _check_for_skipped_scenarios(feature: Feature) -> int:
        try:
            with open(os.path.abspath(feature.uri), "r", encoding="utf-8") as f:
                lines = f.readlines()

            if not lines:
                return 0

            scenario_file_names = [
                line.split(":")[1].strip()
                for line in lines
                if line.strip().startswith("Scenario")
            ]
            scenario_names = [scenario.name for scenario in feature.scenarios]

            skipped = sum(
                1 for name in scenario_file_names if name not in scenario_names
            )
            for name in scenario_file_names:
                if name not in scenario_names:
                    feature.add_scenario(
                        Scenario(
                            id="",
                            name=name,
                            line=0,
                            description="",
                            tags=[],
                            steps=[],
                            status=Status.SKIPPED,
                        )
                    )
            return skipped
        except:
            return 0
