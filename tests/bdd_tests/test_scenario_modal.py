from pytest_bdd import given, when, then, scenarios
from playwright.sync_api import Page, expect
from utils.helpers import scroll_into_view

scenarios("../features/report_modal.feature")


@given("the report is open with a failed scenario")
def setup_report_with_failed_scenario(page: Page):
    page.goto("http://localhost:3000/report")  # Replace with actual page URL


@when("I open the failed scenarios modal")
def open_failed_scenarios_modal(page: Page):
    # Assume the button is accessible as a "button" with a name like "Show Failed Scenarios"
    modal_button = page.get_by_role("button", name="Show Failed Scenarios")
    scroll_into_view(modal_button)
    modal_button.click()


@then("the modal should be visible")
def verify_modal_visible(page: Page):
    # Assuming the modal has role="dialog" and a name like "Failed Scenarios"
    modal = page.get_by_role("dialog", name="Failed Scenarios")
    expect(modal).to_be_visible()


@when("I close the modal")
def close_modal(page: Page):
    # Close button inside the modal
    close_button = page.get_by_role("button", name="Close")
    close_button.click()


@then("the modal should not be visible")
def verify_modal_not_visible(page: Page):
    modal = page.get_by_role("dialog", name="Failed Scenarios")
    expect(modal).not_to_be_visible()