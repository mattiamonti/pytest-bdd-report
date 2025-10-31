import pytest
from tests.bdd.fixtures.setup_fixtures import *
import uuid
from playwright.sync_api import Page
from pytest_bdd_report import attach


@pytest.fixture
def get_uuid():
    def _generate():
        return str(uuid.uuid4()).replace("-", "")[:8]

    return _generate


# To attach playwright screenshot
@pytest.hookimpl(hookwrapper=True)
def pytest_bdd_step_error(
    request, feature, scenario, step, step_func, step_func_args, exception
):
    yield
    for fixture in step_func_args.values():
        page: Page | None = getattr(fixture, "page", None)
        if page:
            # ATTACH SCREENSHOT FROM BYTES
            screen_bytes = page.screenshot()
            # pytest-bdd-report code to attach the screenshot
            attach.screenshot(screen_bytes, feature.name, scenario.name)

            # ATTACH SCREENSHOT FROM IMAGE FILE
            # screenshot_name = "caricamento_image_file.png"
            # screenshot_path = "screen_path/" + screenshot_name

            # _ = page.screenshot(path=screenshot_path)
            # # pytest-bdd-report code to attach the screenshot
            # attach.screenshot(screenshot_path, feature.name, scenario.name)
