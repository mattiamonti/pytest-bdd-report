from pytest_bdd import given
from playwright.sync_api import Page
import pytest
from tests.bdd.utils.open_report_file import open_report_file_with_retry


@given("the report is open with a failed scenario")
def setup_report_with_failed_scenario(
    page: Page, generate_custom_bdd_report, cleanup_bdd_generated
):
    report_structure = {"Feature 1": {"passed": ["Passed 1"], "failed": ["Failed 2"]}}
    report_url = generate_custom_bdd_report(report_structure)
    open_report_file_with_retry(page, report_url)


@given("the report is open with a passed scenario")
def setup_report_with_passed_scenario(
    page: Page, generate_custom_bdd_report, cleanup_bdd_generated
):
    report_structure = {"Feature 1": {"passed": ["Passed 1"]}}
    report_url = generate_custom_bdd_report(report_structure)
    open_report_file_with_retry(page, report_url)


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
    open_report_file_with_retry(page, report_url)
