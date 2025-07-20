from pytest_bdd import then
from playwright.sync_api import Page, expect

@then("the modal should be visible")
def verify_modal_visible(page: Page):
    expect(page.get_by_role("dialog")).to_be_visible()

@then("the modal should not be visible")
def verify_modal_not_visible(page: Page):
    expect(page.get_by_role("dialog")).not_to_be_visible()