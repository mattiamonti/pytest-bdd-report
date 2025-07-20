from pytest_bdd import then, parsers
from playwright.sync_api import Page, expect

@then(parsers.cfparse('the scenario "{name}" should be visible'))
def scenario_should_be_visible(page: Page, name: str):
    scenario = page.locator(f"//*[@id='{name}']/div")
    expect(scenario).to_be_in_viewport()
