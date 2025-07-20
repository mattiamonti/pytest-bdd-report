from pytest_bdd import given, when, then, scenarios, parsers
from playwright.sync_api import Page, expect, Locator
from tests.bdd_generator.bdd_generator import (
    BDDFeature,
    BDDTestBuilder,
    BDDScenario,
    create_failed_step,
    create_passed_step,
    create_skipped_step,
)
import os
import time
import pytest
import tests.bdd_utils.scenario_utils as scenario

scenarios("../bdd_feature/scenario_modal.feature")


@given("the report is open with a failed scenario")
def setup_report_with_failed_scenario(
    page: Page, generate_custom_bdd_report, cleanup_bdd_generated
):
    report_structure = {"Feature 1": {"passed": ["Passed 1"], "failed": ["Failed 2"]}}

    report_url = generate_custom_bdd_report(report_structure)
    page.goto(report_url)


@given("the report is open with a passed scenario")
def setup_report_with_passed_scenario(
    page: Page, generate_custom_bdd_report, cleanup_bdd_generated
):
    report_structure = {"Feature 1": {"passed": ["Passed 1"]}}

    report_url = generate_custom_bdd_report(report_structure)
    page.goto(report_url)


@given("the report is open with multiple failed scenarios")
def setup_report_with_multiple_failed_scenarios(
    page: Page, generate_custom_bdd_report, cleanup_bdd_generated
):
    report_structure = {
        "Feature 1": {
            "passed": ["Passed 4"],
            "failed": ["Failed 1", "Failed 2", "Failed 3"],
        },
        "Feature 2": {"passed": ["Scenario 5"], "failed": []},
    }

    report_url = generate_custom_bdd_report(report_structure)
    page.goto(report_url)


@pytest.fixture
def modal(page: Page):
    return page.get_by_role("dialog")


@when("I open the failed scenarios modal")
def open_failed_scenarios_modal(page: Page):
    # Assume the button is accessible as a "button" with a name like "Show Failed Scenarios"
    # modal_button = page.get_by_role("button", name="Show Failed Scenarios")
    modal_button = page.locator("//*[contains(@class, 'failed-scenarios-link')]")
    modal_button.click()


@then("the feature scenarios link should be visible")
def check_failed_scenarios_link_visibility(page: Page):
    modal_button = page.locator("//*[contains(@class, 'failed-scenarios-link')]")
    expect(modal_button).to_be_visible()


@then("the feature scenarios link should not be visible")
def check_failed_scenarios_link_visibility(page: Page):
    modal_button = page.locator("//*[contains(@class, 'failed-scenarios-link')]")
    expect(modal_button).not_to_be_visible()


@then("the modal should be visible")
def verify_modal_visible(page: Page):
    # Assuming the modal has role="dialog" and a name like "Failed Scenarios"
    modal = page.get_by_role("dialog")
    expect(modal).to_be_visible()


@when("I close the modal")
def close_modal(page: Page):
    # Close button inside the modal
    # close_button = page.get_by_role("button", name="Close")
    close_button = page.locator("//dialog//button[contains(@class, 'modal-close')]")
    close_button.click()


@then(parsers.cfparse("the modal should contain {expected:d} link"))
def check_number_of_links_in_modal(page: Page, expected: int, modal):
    links = modal.locator("a")
    expect(links).to_have_count(expected)


@then(parsers.cfparse('the modal should contain link with text "{expected}"'))
def check_text_of_links_in_modal(page: Page, expected: str, modal: Locator):
    link = modal.get_by_role("link").get_by_text(expected)
    expect(link).to_be_visible()

@when(parsers.cfparse('I click on the link "{name}"'))
def click_on_link_in_modal(modal: Locator, name: str):
    link = modal.get_by_role("link").get_by_text(name)
    assert link.is_visible()
    link.click()


@then(parsers.cfparse('the scenario "{name}" should be visible'))
def verify_scenario_is_visible(page: Page, name: str):
    scenario = page.locator(f"//*[@id='{name}']/div")
    scenario.is_visible()
    expect(scenario).to_be_in_viewport()

@then("the modal should not be visible")
def verify_modal_not_visible(page: Page):
    modal = page.get_by_role("dialog")
    expect(modal).not_to_be_visible()
