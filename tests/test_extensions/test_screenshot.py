from pathlib import Path
import pytest
from pytest_bdd_report.extensions.screenshot import ScreenshotRepo
from pytest_bdd_report.extensions.encoder import Base64Encoder
from hypothesis import given
from hypothesis import strategies as st


@pytest.fixture()
def screenshot_repo():
    return ScreenshotRepo(encoder=Base64Encoder)


@given(
    feature_name=st.text(min_size=1),
    scenario_name=st.text(min_size=1),
    image_data=st.binary(min_size=1),
)
def test_add_screenshot(feature_name: str, scenario_name: str, image_data: bytes):
    screenshot_repo = ScreenshotRepo(encoder=Base64Encoder)

    # Add a new screenshot
    screenshot_repo.add(feature_name, scenario_name, image_data)

    # Check that the screenshot was added to the repository
    assert len(screenshot_repo.repo) == 1
    added_screenshot = screenshot_repo.get(feature_name, scenario_name)
    assert added_screenshot is not None
    assert added_screenshot.feature_name == feature_name
    assert added_screenshot.scenario_name == scenario_name
    assert added_screenshot.encoded_image


@pytest.mark.parametrize(
    "image_path",
    [
        "tests/data/screenshot.png",
        "tests/data/screenshot.jpg",
        "tests/data/screenshot.jpeg",
        Path("tests/data/screenshot.png"),
        Path("tests/data/screenshot.jpg"),
        Path("tests/data/screenshot.jpeg"),
    ],
)
def test_add_screenshot_by_path(image_path: str | Path):
    screenshot_repo = ScreenshotRepo(encoder=Base64Encoder)
    feature_name = "My feature"
    scenario_name = "My scenario"

    # Add a new screenshot
    screenshot_repo.add_by_path(feature_name, scenario_name, image_path)

    # Check that the screenshot was added to the repository
    assert len(screenshot_repo.repo) == 1
    added_screenshot = screenshot_repo.get(feature_name, scenario_name)
    assert added_screenshot is not None
    assert added_screenshot.feature_name == feature_name
    assert added_screenshot.scenario_name == scenario_name
    assert added_screenshot.encoded_image is None
    assert added_screenshot.path == str(Path(image_path).absolute())


def test_add_screenshot_by_path_and_by_data_should_fail():
    screenshot_repo = ScreenshotRepo(encoder=Base64Encoder)
    feature_name = "My feature"
    scenario_name = "My scenario"
    image_path = "tests/data/screenshot.png"
    image_data = b"Sample image"

    # Add a new screenshot
    screenshot_repo.add(feature_name, scenario_name, image_data)
    with pytest.raises(ValueError):
        screenshot_repo.add_by_path(feature_name, scenario_name, image_path)

    # Check that the screenshot was added to the repository
    assert len(screenshot_repo.repo) == 1
    added_screenshot = screenshot_repo.get(feature_name, scenario_name)
    assert added_screenshot is not None
    assert added_screenshot.encoded_image
    assert added_screenshot.path is None


@pytest.mark.parametrize(
    "feature_name_1, scenario_name_1, image_data_1, feature_name_2, scenario_name_2, image_data_2",
    [
        (
            "My feature",
            "My scenario",
            b"Sample image data",
            "Different feature",
            "Different scenario",
            b"Different image data",
        ),
        (
            "My feature",
            "My scenario",
            b"Sample image data",
            "My feature",
            "Different scenario",
            b"Different image data",
        ),
        (
            "My feature",
            "My scenario",
            b"Sample image data",
            "Different feature",
            "My scenario",
            b"Different image data",
        ),
    ],
)
def test_add_multiple_screenshot(
    screenshot_repo: ScreenshotRepo,
    feature_name_1: str,
    scenario_name_1: str,
    image_data_1: bytes,
    feature_name_2: str,
    scenario_name_2: str,
    image_data_2: bytes,
):
    # Add multiple new screenshot
    screenshot_repo.add(feature_name_1, scenario_name_1, image_data_1)
    screenshot_repo.add(feature_name_2, scenario_name_2, image_data_2)

    # Check that the different screenshot are added to the repository
    assert len(screenshot_repo.repo) == 2
    screenshot_1 = screenshot_repo.get(feature_name_1, scenario_name_1)
    screenshot_2 = screenshot_repo.get(feature_name_2, scenario_name_2)
    assert screenshot_1 is not None
    assert screenshot_2 is not None
    assert screenshot_1.encoded_image != screenshot_2.encoded_image


def test_get_nonexistent_screenshot(screenshot_repo: ScreenshotRepo):
    feature_name = "My Feature"
    scenario_name = "Non-Existent Scenario"

    # Try to get a non-existent screenshot
    result = screenshot_repo.get(feature_name, scenario_name)
    assert result is None


def test_exists_nonexistent_screenshot(screenshot_repo: ScreenshotRepo):
    feature_name = "My Feature"
    scenario_name = "Non-Existent Scenario"

    # Check that the non-existent screenshot does not exist in the repository
    assert not screenshot_repo.exists(feature_name, scenario_name)


def test_add_duplicate_screenshot(screenshot_repo: ScreenshotRepo):
    feature_name = "My Feature"
    scenario_name = "My Scenario"
    image_data = b"This is some sample image data"

    # Add a new screenshot
    screenshot_repo.add(feature_name, scenario_name, image_data)

    # Try to add the same screenshot again (should raise ValueError)
    with pytest.raises(ValueError):
        screenshot_repo.add(feature_name, scenario_name, image_data)


def test_get_existent_screenshot(screenshot_repo: ScreenshotRepo):
    feature_name = "My Feature"
    scenario_name = "My Scenario"
    image_data = b"This is some sample image data"

    # Add a new screenshot
    screenshot_repo.add(feature_name, scenario_name, image_data)

    # Try to get the existing screenshot
    result = screenshot_repo.get(feature_name, scenario_name)
    assert result is not None
    assert result.feature_name == feature_name
    assert result.scenario_name == scenario_name
    assert result.encoded_image
