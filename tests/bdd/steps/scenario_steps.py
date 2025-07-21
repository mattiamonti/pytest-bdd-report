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
