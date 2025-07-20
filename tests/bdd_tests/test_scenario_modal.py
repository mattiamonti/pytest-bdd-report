from pytest_bdd import given, when, then, scenarios, parsers
from playwright.sync_api import Page, expect, Locator
from tests.bdd_generator.bdd_generator import BDDFeature, BDDTestBuilder, BDDScenario, create_failed_step, create_passed_step, create_skipped_step
import os
import time
import pytest

scenarios("../bdd_feature/scenario_modal.feature")


@given("the report is open with a failed scenario")
def setup_report_with_failed_scenario(page: Page, cleanup_bdd_generated):
    builder = BDDTestBuilder("generated_tests")
    feature = BDDFeature("Testing failed scenarios links")
    scenario1 = BDDScenario("Failed 1")
    scenario1.add_step(create_passed_step("lo step è passato"))
    scenario1.add_step(create_passed_step("lo step è passato"))
    scenario1.add_step(create_failed_step("lo step è fallito"))
    feature.add_scenario(scenario1)
    scenario2 = BDDScenario("Failed 2")
    scenario2.add_step(create_passed_step("lo step è passato"))
    scenario2.add_step(create_passed_step("lo step è passato"))
    scenario2.add_step(create_failed_step("lo step è fallito"))
    feature.add_scenario(scenario2)
    scenario3 = BDDScenario("Failed 3")
    scenario3.add_step(create_passed_step("lo step è passato"))
    scenario3.add_step(create_passed_step("lo step è passato"))
    scenario3.add_step(create_failed_step("lo step è fallito"))
    feature.add_scenario(scenario3)
    builder.add_feature(feature)
    builder.build()

    os.system("pytest --bdd-report=proto_bdd_testing.html generated_tests/")

    path = os.path.abspath("proto_bdd_testing.html")
    file_url = "file://" + path

    page.goto(file_url)  # Replace with actual page URL
    time.sleep(1)

@pytest.fixture
def modal(page: Page):
    return page.get_by_role("dialog")


@when("I open the failed scenarios modal")
def open_failed_scenarios_modal(page: Page):
    # Assume the button is accessible as a "button" with a name like "Show Failed Scenarios"
    #modal_button = page.get_by_role("button", name="Show Failed Scenarios")
    modal_button = page.locator("//*[contains(@class, 'failed-scenarios-link')]")
    modal_button.click()


@then("the modal should be visible")
def verify_modal_visible(page: Page):
    # Assuming the modal has role="dialog" and a name like "Failed Scenarios"
    modal = page.get_by_role("dialog")
    expect(modal).to_be_visible()


@when("I close the modal")
def close_modal(page: Page):
    # Close button inside the modal
    #close_button = page.get_by_role("button", name="Close")
    close_button = page.locator("//dialog//button[contains(@class, 'modal-close')]")
    close_button.click()

@then(parsers.cfparse(
    'the modal should contain {expected:d} link'
))
def check_number_of_links_in_modal(page: Page, expected: int, modal):
    links = modal.locator("a")
    expect(links).to_have_count(expected)

@then(parsers.cfparse(
    'the modal should contain link with text "{expected}"'
))
def check_text_of_links_in_modal(page: Page, expected: str, modal: Locator):
    link = modal.get_by_role("link").get_by_text(expected)
    expect(link).to_be_visible()

@then("the modal should not be visible")
def verify_modal_not_visible(page: Page):
    modal = page.get_by_role("dialog")
    expect(modal).not_to_be_visible()