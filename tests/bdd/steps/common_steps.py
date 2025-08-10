from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page, expect
from tests.bdd.elements.report_pom import ReportPOM
import pytest


@when("I scroll to the bottom")
def scroll_to_bottom(page: Page):
    page.evaluate("window.scrollTo(0,document.body.scrollHeight)")
    page.wait_for_timeout(2000)  # wait for 2s to scroll all the way down


@then("the report should be at the top")
def report_top(page: Page):
    page.get_by_role("heading").get_by_text("Report")

@when(parsers.parse("I collapse all the scenarios"))
def collapse_all_scenarios(page: Page):
    report = ReportPOM(page)
    report.collapse_all_scenarios()

@when(parsers.parse("I expand all the scenarios"))
def expand_all_scenarios(page: Page):
    report = ReportPOM(page)
    report.expand_all_scenarios()
