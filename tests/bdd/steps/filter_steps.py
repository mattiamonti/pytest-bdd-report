from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page, expect
from tests.bdd.elements.filter_pom import FilterPOM
from tests.bdd.elements.report_pom import ReportPOM
import pytest


@then(parsers.cfparse("the '{name}' filter should be enabled"))
def filter_enabled(page: Page, name: str):
    filter = FilterPOM(page, name)
    filter.should_be_enabled()


@then(parsers.cfparse("the '{name}' filter should not be enabled"))
def filter_not_enabled(page: Page, name: str):
    filter = FilterPOM(page, name)
    filter.should_not_be_enabled()


@when(parsers.cfparse("I toggle the '{name}' filter"))
def toggle_filter(page: Page, name: str):
    filter = FilterPOM(page, name)
    filter.toggle()


@then(parsers.cfparse("the {scenario_type} scenarios should be hidden"))
def scenario_type_should_be_hidden(page: Page, scenario_type: str):
    assert scenario_type in ["passed", "failed", "skipped"]
    report = ReportPOM(page)
    match scenario_type:
        case "passed":
            expect(report.get_passed_scenarios()).to_be_hidden()
        case "failed":
            expect(report.get_failed_scenarios()).to_be_hidden()
        case "skipped":
            expect(report.get_skipped_scenarios()).to_be_hidden()


@then(parsers.cfparse("the {scenario_type} scenarios should be visible"))
def scenario_type_should_be_hidden(page: Page, scenario_type: str):
    assert scenario_type in ["passed", "failed", "skipped"]
    report = ReportPOM(page)
    match scenario_type:
        case "passed":
            expect(report.get_passed_scenarios()).not_to_be_hidden()
        case "failed":
            expect(report.get_failed_scenarios()).not_to_be_hidden()
        case "skipped":
            expect(report.get_skipped_scenarios()).not_to_be_hidden()
