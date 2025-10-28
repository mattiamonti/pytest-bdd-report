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
def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    yield
    for fixture in step_func_args.values():
        page = getattr(fixture, 'page', None) 
        if page:
            #TODO implementare il caricamento degli screenshot da file immagine, per ora funziona con l'immagine in bytes
            #screenshot_name = "prova_nome_1.png"
            #screenshot_path = "screen_path/"+screenshot_name

            screen_bytes = page.screenshot()

            # pytest-bdd-report code to attach the screenshot
            attach.screenshot(screen_bytes, feature.name, scenario.name)