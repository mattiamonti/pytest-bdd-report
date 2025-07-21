from pytest_bdd import then, parsers
from playwright.sync_api import Page, expect
from tests.bdd.elements.scenario_pom import ScenarioPOM
import pytest


@pytest.fixture
def scenario(page: Page):
    return ScenarioPOM(page)


@then(parsers.cfparse('the scenario "{name}" should be visible'))
def scenario_should_be_visible(scenario: ScenarioPOM, name: str):
    scenario.should_be_visible(name)


@then(parsers.cfparse('the scenario "{name}" should be passed'))
def scenario_should_be_visible(scenario: ScenarioPOM, name: str):
    scenario.is_passed(name)


@then(parsers.cfparse('the scenario "{name}" should be failed'))
def scenario_should_be_visible(scenario: ScenarioPOM, name: str):
    scenario.is_failed(name)


@then(parsers.cfparse('the scenario "{name}" should be skipped'))
def scenario_should_be_visible(scenario: ScenarioPOM, name: str):
    scenario.is_skipped(name)
