from pytest_bdd import when, then, parsers
from playwright.sync_api import Page, Locator, expect
import pytest
from tests.bdd.elements.failed_scenarios_modal import FailedScenariosModalPOM
from tests.bdd.elements.feature_pom import FeaturePOM


@pytest.fixture
def failed_scenarios_modal(page: Page):
    return FailedScenariosModalPOM(page)


@when("I open the failed scenarios modal")
def open_modal(failed_scenarios_modal: FailedScenariosModalPOM):
    failed_scenarios_modal.open()


@when(parsers.cfparse("I open the failed scenarios modal for the feature '{name}'"))
def open_modal_for_feature(page: Page, name: str):
    feature = FeaturePOM(page, name)
    modal = FailedScenariosModalPOM(feature.get())
    modal.open()


@when("I close the modal")
def close_modal(failed_scenarios_modal: FailedScenariosModalPOM):
    failed_scenarios_modal.close()


@then("the modal should be visible")
def verify_modal_visible(failed_scenarios_modal: FailedScenariosModalPOM):
    failed_scenarios_modal.should_be_visible()


@then("the modal should not be visible")
def verify_modal_not_visible(failed_scenarios_modal: FailedScenariosModalPOM):
    failed_scenarios_modal.should_not_be_visible()


@then("the feature scenarios link should be visible")
def feature_link_visible(failed_scenarios_modal: FailedScenariosModalPOM):
    failed_scenarios_modal.open_button_should_be_visible()


@then("the feature scenarios link should not be visible")
def feature_link_not_visible(failed_scenarios_modal: FailedScenariosModalPOM):
    failed_scenarios_modal.open_button_should_not_be_visible()


@then(parsers.cfparse("the modal should contain {expected:d} link"))
def modal_contains_links(
    failed_scenarios_modal: FailedScenariosModalPOM, expected: int
):
    expect(failed_scenarios_modal.get_links()).to_have_count(expected)


@then(parsers.cfparse('the modal should contain link with text "{expected}"'))
def modal_contains_link_text(
    failed_scenarios_modal: FailedScenariosModalPOM, expected: str
):
    failed_scenarios_modal.should_contain_link(expected)


@when(parsers.cfparse('I click on the link "{name}"'))
def click_link(failed_scenarios_modal: FailedScenariosModalPOM, name: str):
    failed_scenarios_modal.click_on_link(name)
