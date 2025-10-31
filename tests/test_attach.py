import pytest
from hypothesis import given
from hypothesis import strategies as st
from pytest_bdd_report import attach
from pytest_bdd_report.extensions.screenshot import screenshot_repo


@given(
    feature_name=st.text(min_size=1),
    scenario_name=st.text(min_size=1),
    image_data=st.binary(min_size=1),
)
def test_attach_screenshot(feature_name: str, scenario_name: str, image_data: bytes):
    attach.screenshot(image_data, feature_name, scenario_name)

    assert len(screenshot_repo.repo) == 1
    added_screenshot = screenshot_repo.get(feature_name, scenario_name)
    assert added_screenshot is not None
    assert added_screenshot.feature_name == feature_name
    assert added_screenshot.scenario_name == scenario_name
    assert added_screenshot.encoded_image
    screenshot_repo.repo = []  # Clean the repository after the test


@given(
    feature_name=st.text(min_size=1),
    scenario_name=st.text(min_size=1),
)
@pytest.mark.parametrize(
    "screenshot_path",
    [
        "tests/data/screenshot.png",
        "tests/data/screenshot.jpeg",
        "tests/data/screenshot.jpg",
    ],
)
def test_attach_screenshot_file_png(
    feature_name: str, scenario_name: str, screenshot_path: str
):
    attach.screenshot_file(screenshot_path, feature_name, scenario_name)

    assert len(screenshot_repo.repo) == 1
    added_screenshot = screenshot_repo.get(feature_name, scenario_name)
    assert added_screenshot is not None
    assert added_screenshot.feature_name == feature_name
    assert added_screenshot.scenario_name == scenario_name
    assert added_screenshot.encoded_image
    screenshot_repo.repo = []  # Clean the repository after the test
