import pytest
import base64
from pytest_bdd_report import attach
from pytest_bdd_report.screenshot import screenshot_repo, ScreenshotRepo

@pytest.fixture
def mock_bytes() -> bytes:
    return b"mock bytes"

@pytest.fixture
def feature_name() -> str:
    return "feature 1"

@pytest.fixture
def scenario_name() -> str:
    return "scenario 1"

@pytest.fixture
def teardown():
    screenshot_repo.repo = []



def test_attach_screenshot_from_bytes_is_saved(mock_bytes, feature_name, scenario_name, teardown):
    attach.screenshot(mock_bytes, feature_name, scenario_name)

    assert len(screenshot_repo.repo) == 1
    assert screenshot_repo.get(feature_name, scenario_name) != None
    assert screenshot_repo.get(feature_name, scenario_name) != ""


def test_encoding_of_screenshot_from_bytes(mock_bytes, feature_name, scenario_name, teardown):
    attach.screenshot(mock_bytes, feature_name, scenario_name)
    image_base64 = screenshot_repo.get(feature_name, scenario_name)
    
    assert isinstance(image_base64, str)
    assert image_base64 == base64.b64encode(mock_bytes).decode("utf-8")
    assert mock_bytes == base64.b64decode(image_base64)


def test_retrieving_screenshot_attached_from_bytes(mock_bytes, feature_name, scenario_name, teardown):
    attach.screenshot(mock_bytes, feature_name, scenario_name)
    valid_research = screenshot_repo.get(feature_name, scenario_name)
    invalid_research_feature = screenshot_repo.get("invalid", scenario_name)
    invalid_research_scenario = screenshot_repo.get(feature_name, "invalid")
    invalid_research_scenario_and_feature = screenshot_repo.get("invalid", "invalid")

    assert valid_research != None
    assert invalid_research_feature == None
    assert invalid_research_scenario == None
    assert invalid_research_scenario_and_feature == None


def test_retrieving_screenshot_with_multiple_saved_with_same_feature(mock_bytes, feature_name, scenario_name, teardown):
    second_bytes = b"second screenshot"

    attach.screenshot(mock_bytes, feature_name, scenario_name)
    attach.screenshot(second_bytes, feature_name, "scenario 2")

    first_image = screenshot_repo.get(feature_name, scenario_name)
    second_image = screenshot_repo.get(feature_name, "scenario 2")

    assert len(screenshot_repo.repo) == 2
    assert mock_bytes == base64.b64decode(first_image)
    assert  second_bytes == base64.b64decode(second_image)


def test_add_more_screenshot_with_same_feature_and_scenario_should_fail(mock_bytes, feature_name, scenario_name, teardown):
    attach.screenshot(mock_bytes, feature_name, scenario_name)
    
    with pytest.raises(RuntimeWarning):
        attach.screenshot(mock_bytes, feature_name, scenario_name)

    assert len(screenshot_repo.repo) == 1
    
def test_add_more_screenshot_with_same_feature_and_different_scenario(mock_bytes, feature_name, scenario_name, teardown):
    attach.screenshot(mock_bytes, feature_name, scenario_name)
    attach.screenshot(mock_bytes, feature_name, "scenario 2")

    assert len(screenshot_repo.repo) == 2

def test_add_more_screenshot_with_same_scenario_and_different_feature(mock_bytes, feature_name, scenario_name, teardown):
    attach.screenshot(mock_bytes, feature_name, scenario_name)
    attach.screenshot(mock_bytes, "feature 2", scenario_name)

    assert len(screenshot_repo.repo) == 2