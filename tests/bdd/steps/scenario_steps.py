from pytest_bdd import then, when, parsers
from playwright.sync_api import Page, expect
from tests.bdd.elements.scenario_pom import ScenarioPOM
import pytest


@then(parsers.cfparse('the scenario "{name}" should be visible'))
def scenario_should_be_visible(page: Page, name: str):
    scenario = ScenarioPOM(page, name)
    scenario.should_be_visible()


@then(parsers.cfparse('the scenario "{name}" should be passed'))
def scenario_should_be_visible(page: Page, name: str):
    scenario = ScenarioPOM(page, name)
    scenario.is_passed()


@then(parsers.cfparse('the scenario "{name}" should be failed'))
def scenario_should_be_visible(page: Page, name: str):
    scenario = ScenarioPOM(page, name)
    scenario.is_failed()


@then(parsers.cfparse('the scenario "{name}" should be skipped'))
def scenario_should_be_visible(page: Page, name: str):
    scenario = ScenarioPOM(page, name)
    scenario.is_skipped()


@then(parsers.cfparse("the scenario '{name}' should have {scenario_type} color"))
def scenario_should_be_visible(page: Page, name: str, scenario_type: str):
    scenario = ScenarioPOM(page, name)
    scenario.background_should_be(scenario_type)


@then(parsers.cfparse("the scenario '{name}' error message should be hidden"))
def error_message_should_be_hidden(page: Page, name: str):
    scenario = ScenarioPOM(page, name)
    scenario.error_message_should_be_hidden()


@then(parsers.cfparse("the scenario '{name}' error message should be visible"))
def error_message_should_be_visible(page: Page, name: str):
    scenario = ScenarioPOM(page, name)
    scenario.error_message_should_be_visible()


@when(parsers.cfparse("I toggle the scenario '{name}' error message"))
def toggle_error_message(page: Page, name: str):
    scenario = ScenarioPOM(page, name)
    scenario.toggle_error_message()


@then(parsers.parse("the scenario '{name}' duration should not be zero"))
def feature_duration(page: Page, name: str):
    scenario = ScenarioPOM(page, name)
    duration = scenario.get_duration()
    assert duration > 0.0


@then(parsers.parse("the scenario '{name}' duration should be zero"))
def scenario_duration(page: Page, name: str):
    scenario = ScenarioPOM(page, name)
    duration = scenario.get_duration()
    assert duration == 0.0


@when(parsers.parse("I expand the scenario '{name}'"))
def scenario_duration(page: Page, name: str):
    scenario = ScenarioPOM(page, name)
    scenario.get().scroll_into_view_if_needed()
    scenario.expand()


@when(parsers.parse("I collapse the scenario '{name}'"))
def scenario_duration(page: Page, name: str):
    scenario = ScenarioPOM(page, name)
    scenario.get().scroll_into_view_if_needed()
    scenario.collapse()


@then(parsers.parse("the steps are visible for the scenario '{name}'"))
def scenario_duration(page: Page, name: str):
    scenario = ScenarioPOM(page, name)
    scenario.get().scroll_into_view_if_needed()
    steps = scenario.get_steps("passed")
    steps.extend(scenario.get_steps("failed"))
    for step in steps:
        expect(step).to_be_visible()
        expect(step).to_be_in_viewport()


@then(parsers.parse("the steps are not visible for the scenario '{name}'"))
def scenario_duration(page: Page, name: str):
    scenario = ScenarioPOM(page, name)
    scenario.get().scroll_into_view_if_needed()
    steps = scenario.get_steps("passed")
    steps.extend(scenario.get_steps("failed"))
    for step in steps:
        expect(step).not_to_be_visible()
        expect(step).not_to_be_in_viewport()
