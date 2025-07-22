from pytest_bdd import then, parsers
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
