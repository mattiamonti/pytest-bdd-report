from pytest_bdd import then, when, parsers
from playwright.sync_api import Page, expect
from tests.bdd.elements.file_list_pom import FileListPOM
import pytest


@when("I click on the test file paths button")
def toggle_test_file_paths(page: Page):
    file_list = FileListPOM(page)
    file_list.click()


@then("the test file paths should be visible")
def file_list_visible(page: Page):
    file_list = FileListPOM(page)
    file_list.should_be_visible()


@then("the test file paths should be hidden")
def file_list_hidden(page: Page):
    file_list = FileListPOM(page)
    file_list.should_be_hidden()


@then(parsers.cfparse("the test file paths should contain the path '{path}'"))
def file_list_contains(page: Page, path: str):
    file_list = FileListPOM(page)
    file_list.should_contain(path)
