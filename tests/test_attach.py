from pathlib import Path
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
    screenshot_repo.repo.remove(added_screenshot)  # Clean the repository after the test
    assert added_screenshot.feature_name == feature_name
    assert added_screenshot.scenario_name == scenario_name
    assert added_screenshot.encoded_image


@given(
    feature_name=st.text(min_size=1),
    scenario_name=st.text(min_size=1),
)
def test_attach_screenshot_file(feature_name: str, scenario_name: str):
    screenshot_path = "tests/data/screenshot.png"

    attach.screenshot(screenshot_path, feature_name, scenario_name)

    assert len(screenshot_repo.repo) == 1
    added_screenshot = screenshot_repo.get(feature_name, scenario_name)
    assert added_screenshot is not None
    screenshot_repo.repo.remove(added_screenshot)  # Clean the repository after the test
    assert added_screenshot.feature_name == feature_name
    assert added_screenshot.scenario_name == scenario_name
    assert added_screenshot.path == str(Path(screenshot_path).absolute())


@pytest.mark.parametrize(
    "screenshot_path",
    [
        "tests/data/screenshot.png",
        "tests/data/screenshot.jpeg",
        "tests/data/screenshot.jpg",
    ],
)
def test_attach_screenshot_different_file_types_by_str(screenshot_path: str):
    feature_name = "My feature"
    scenario_name = "My scenario"
    attach.screenshot(screenshot_path, feature_name, scenario_name)

    assert len(screenshot_repo.repo) == 1
    added_screenshot = screenshot_repo.get(feature_name, scenario_name)
    assert added_screenshot is not None
    screenshot_repo.repo.remove(added_screenshot)  # Clean the repository after the test
    assert added_screenshot.feature_name == feature_name
    assert added_screenshot.scenario_name == scenario_name
    assert added_screenshot.path == str(Path(screenshot_path).absolute())


@pytest.mark.parametrize(
    "screenshot_path",
    [
        Path("tests/data/screenshot.png"),
        Path("tests/data/screenshot.jpeg"),
        Path("tests/data/screenshot.jpg"),
    ],
)
def test_attach_screenshot_different_file_types_by_path(screenshot_path: Path):
    feature_name = "My feature"
    scenario_name = "My scenario"
    attach.screenshot(screenshot_path, feature_name, scenario_name)

    assert len(screenshot_repo.repo) == 1
    added_screenshot = screenshot_repo.get(feature_name, scenario_name)
    assert added_screenshot is not None
    screenshot_repo.repo.remove(added_screenshot)  # Clean the repository after the test
    assert added_screenshot.feature_name == feature_name
    assert added_screenshot.scenario_name == scenario_name
    assert added_screenshot.path == str(screenshot_path.absolute())
