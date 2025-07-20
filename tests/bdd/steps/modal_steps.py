from pytest_bdd import when, then, parsers
from playwright.sync_api import Page, Locator, expect

@when("I open the failed scenarios modal")
def open_modal(page: Page):
    page.locator("//*[contains(@class, 'failed-scenarios-link')]").click()

@when("I close the modal")
def close_modal(page: Page):
    page.locator("//dialog//button[contains(@class, 'modal-close')]").click()

@then("the feature scenarios link should be visible")
def feature_link_visible(page: Page):
    expect(page.locator("//*[contains(@class, 'failed-scenarios-link')]")).to_be_visible()

@then("the feature scenarios link should not be visible")
def feature_link_not_visible(page: Page):
    expect(page.locator("//*[contains(@class, 'failed-scenarios-link')]")).not_to_be_visible()

@then(parsers.cfparse("the modal should contain {expected:d} link"))
def modal_contains_links(modal: Locator, expected: int):
    expect(modal.locator("a")).to_have_count(expected)

@then(parsers.cfparse('the modal should contain link with text "{expected}"'))
def modal_contains_link_text(modal: Locator, expected: str):
    expect(modal.get_by_role("link").get_by_text(expected)).to_be_visible()

@when(parsers.cfparse('I click on the link "{name}"'))
def click_link(modal: Locator, name: str):
    link = modal.get_by_role("link").get_by_text(name)
    assert link.is_visible()
    link.click()