from pytest_bdd import given, when, then, scenarios, parsers
from playwright.sync_api import Page, expect, Locator


@then(parsers.cfparse('the scenario "{name}" should be visible'))
def verify_scenario_is_visible(page: Page, name: str):
    scenario = page.locator(f"//*[@id='{name}']/div")
    scenario.is_visible()
