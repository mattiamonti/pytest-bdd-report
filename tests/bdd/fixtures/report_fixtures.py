import pytest
from playwright.sync_api import Page

@pytest.fixture
def modal(page: Page):
    return page.get_by_role("dialog")