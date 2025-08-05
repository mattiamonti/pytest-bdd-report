from pytest_bdd import when, then, parsers
from playwright.sync_api import Page, Locator, expect
import pytest
from tests.bdd.elements.return_to_top_pom import ReturnToTopPOM


@pytest.fixture
def return_to_top(page: Page):
    return ReturnToTopPOM(page)


@when("I click the return to top button")
def click_return_to_top(return_to_top: ReturnToTopPOM):
    return_to_top.click()


@when("I hover on the return to top button")
def hover_return_to_top(return_to_top: ReturnToTopPOM):
    return_to_top.hover()


@then(parsers.cfparse("the button should contain text '{text}'"))
def hover_text(return_to_top: ReturnToTopPOM, text: str):
    return_to_top.should_display_text(text)


@then(parsers.cfparse("the button should not contain text '{text}'"))
def hover_text(return_to_top: ReturnToTopPOM, text: str):
    return_to_top.should_not_display_text(text)
