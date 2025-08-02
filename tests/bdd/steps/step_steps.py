from pytest_bdd import then, when, parsers
from playwright.sync_api import Page, expect
from tests.bdd.elements.scenario_pom import ScenarioPOM
from tests.bdd.elements.step_pom import StepPOM
import pytest


@then(
    parsers.cfparse("the scenario '{name}' should have {quantity:d} {step_type} steps")
)
def should_have_steps(page: Page, name: str, quantity: int, step_type: str):
    scenario = ScenarioPOM(page, name)
    steps = scenario.get_steps(step_type)
    assert len(steps) == quantity


@then(
    parsers.cfparse("the scenario '{name}' {step_type} steps should have text '{text}'")
)
def steps_should_have_text(page: Page, name: str, step_type: str, text: str):
    scenario = ScenarioPOM(page, name)
    steps = scenario.get_steps(step_type)
    for item in steps:
        step = StepPOM(item)
        assert text in step.get_text(), f"Expected '{text}' in '{step.get_text()}'"


@then(
    parsers.cfparse(
        "the scenario '{name}' {step_type} steps duration should not be zero"
    )
)
def steps_duration(page: Page, name: str, step_type: str):
    scenario = ScenarioPOM(page, name)
    steps = scenario.get_steps(step_type)
    if step_type == "failed":
        steps = steps[
            :1
        ]  # Checking the duration only for the first failed steps, as the following steps will not be executed
    for item in steps:
        step = StepPOM(item)
        assert step.get_duration() > 0.0
