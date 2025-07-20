import pytest
from playwright.sync_api import Page

@pytest.fixture
def modal(page: Page):
    return page.get_by_role("dialog")

@pytest.fixture
def modal_button(page: Page):
    return page.locator("//*[contains(@class, 'failed-scenarios-link')]")

@pytest.fixture
def modal_close(page: Page):
    return page.locator("//dialog//button[contains(@class, 'modal-close')]")
