from src.pytest_bdd_report.components.scenario import Scenario
from src.pytest_bdd_report.components.step import Step


def test_add_step():
    scenario = Scenario(
        id="",
        name="",
        line=0,
        description="",
        tags=[],
        steps=[],
    )
    scenario.add_step(Step("Given", "name", 0, "passed", 0))
    assert scenario.steps == [Step("Given", "name", 0, "passed", 0)]


def test_add_multiple_steps():
    scenario = Scenario(
        id="",
        name="",
        line=0,
        description="",
        tags=[],
        steps=[],
    )
    scenario.add_step(Step("Given", "name", 0, "passed", 0))
    scenario.add_step(Step("When", "name", 0, "passed", 0))
    assert len(scenario.steps) == 2


def test_calculate_duration():
    scenario = Scenario(
        id="",
        name="",
        line=0,
        description="",
        tags=[],
        steps=[],
    )
    scenario.add_step(Step("Given", "name", 0, "passed", 100))
    scenario.add_step(Step("When", "name", 0, "passed", 10))
    expected_duration = (100 + 10) / 1_000_000_000  # from nanosecond to second
    scenario.calculate_duration()
    assert scenario.duration == expected_duration
