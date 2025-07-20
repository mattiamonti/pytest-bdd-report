from pytest_bdd import when, then, parsers
from playwright.sync_api import Page, Locator, expect
import pytest

@pytest.fixture
def modal_button(page: Page):
    return page.locator("//*[contains(@class, 'failed-scenarios-link')]")

@pytest.fixture
def modal_close(page: Page):
    return page.locator("//dialog//button[contains(@class, 'modal-close')]")

@when("I open the failed scenarios modal")
def open_modal(page: Page, modal_button: Locator):
    modal_button.scroll_into_view_if_needed()
    expect(modal_button).to_be_in_viewport()
    modal_button.click()
    
@when("I close the modal")
def close_modal(page: Page, modal_close):
    expect(modal_close).to_be_visible()
    modal_close.click()
    
@then("the modal should be visible")
def verify_modal_visible(page: Page, modal):
    expect(modal).to_be_visible()

@then("the modal should not be visible")
def verify_modal_not_visible(page: Page):
    expect(modal).not_to_be_visible()

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