from abc import ABC, abstractmethod
from pytest_bdd_report.components.feature import Feature
from pytest_bdd_report.components.scenario import Scenario
from pytest_bdd_report.components.step import Step


class BaseExtractor(ABC):
    def extract_from(self, data: list[dict]) -> list:
        """
        Extract the objects from the raw data passed.
        @param data: raw data
        @return: objects extracted
        """
        return [self.create_item(item_data) for item_data in data]

    @abstractmethod
    def create_item(self, data):
        """
        Create one item from the data passed.
        @param data: raw data for one object
        @return: object
        """
        ...


class StepExtractor(BaseExtractor):
    def create_item(self, data) -> Step:
        return Step(
            keyword=data["keyword"],
            name=data["name"],
            line=data["line"],
            status=data["result"]["status"],
            duration=data["result"]["duration"],
        )


class ScenarioExtractor(BaseExtractor):
    def create_item(self, data) -> Scenario:
        steps = StepExtractor().extract_from(data["steps"])
        status = "failed" if self._check_for_failed(steps) else "passed"
        return Scenario(
            id=data["id"],
            name=data["name"],
            line=data["line"],
            description=data["description"],
            tags=data["tags"],
            steps=steps,
            status=status,
        )

    @staticmethod
    def _check_for_failed(items: list[Step] | list[Scenario]) -> bool:
        for item in items:
            if item.status == "failed":
                return True
        return False


class FeatureExtractor(BaseExtractor):
    def create_item(self, data) -> Feature:
        scenarios = ScenarioExtractor().extract_from(data["elements"])
        failed, passed, total = self._count_failed_passed_total_tests(scenarios)
        status = "passed" if failed == 0 else "failed"
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
        feature.set_total_tests(total)
        feature.set_failed_tests(failed)
        feature.set_passed_tests(passed)
        skipped = total - failed - passed
        feature.set_skipped_test(skipped)
        return feature

    @staticmethod
    def _count_failed_passed_total_tests(tests: list) -> tuple[int, int, int]:
        failed = 0
        passed = 0
        total = 0
        for test in tests:
            if test.status == "failed":
                failed += 1
            if test.status == "passed":
                passed += 1
            total += 1
        return failed, passed, total
