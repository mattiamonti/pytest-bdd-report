from pathlib import Path, PosixPath, PurePosixPath, PureWindowsPath, WindowsPath

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
    assert added_screenshot.encoded_image


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
    assert added_screenshot.encoded_image


@pytest.mark.parametrize(
    "screenshot_path",
    [
        Path("tests/data/screenshot.png"),
        Path("tests/data/screenshot.jpeg"),
        Path("tests/data/screenshot.jpg"),
        PosixPath("tests/data/screenshot.png"),
        PosixPath("tests/data/screenshot.jpeg"),
        PosixPath("tests/data/screenshot.jpg"),
        PurePosixPath("tests/data/screenshot.png"),
        PurePosixPath("tests/data/screenshot.jpeg"),
        PurePosixPath("tests/data/screenshot.jpg"),
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
    assert added_screenshot.encoded_image


@pytest.mark.parametrize(
    "screenshot_path",
    [
        PureWindowsPath(r"tests\data\screenshot.png"),
        PureWindowsPath(r"tests\data\screenshot.jpg"),
        PureWindowsPath(r"tests\data\screenshot.jpeg"),
    ],
)
def test_attach_screenshot_file_windows_path(screenshot_path: Path):
    feature_name = "My feature"
    scenario_name = "My scenario"
    attach.screenshot(screenshot_path, feature_name, scenario_name)

    assert len(screenshot_repo.repo) == 1
    added_screenshot = screenshot_repo.get(feature_name, scenario_name)
    assert added_screenshot is not None
    screenshot_repo.repo.remove(added_screenshot)  # Clean the repository after the test
    assert added_screenshot.feature_name == feature_name
    assert added_screenshot.scenario_name == scenario_name
    assert added_screenshot.encoded_image


@pytest.mark.parametrize(
    "screenshot_original, screenshot_duplicated",
    [
        (b"image in bytes", "tests/data/screenshot.png"),
        (b"image in bytes", "tests/data/screenshot.jpeg"),
        (b"image in bytes", "tests/data/screenshot.jpg"),
        ("tests/data/screenshot.png", b"image in bytes"),
        ("tests/data/screenshot.jpeg", b"image in bytes"),
        ("tests/data/screenshot.jpg", b"image in bytes"),
    ],
)
def test_attach_duplicated_screenshot(
    screenshot_original: str | bytes, screenshot_duplicated: str | bytes, capsys
):
    feature_name = "test-feature"
    scenario_name = "test-scenario"

    attach.screenshot(screenshot_original, feature_name, scenario_name)
    attach.screenshot(screenshot_duplicated, feature_name, scenario_name)

    captured = capsys.readouterr()
    assert "Error while attaching the screenshot" in captured.out

    assert len(screenshot_repo.repo) == 1
    added_screenshot = screenshot_repo.get(feature_name, scenario_name)
    assert added_screenshot is not None
    screenshot_repo.repo.remove(added_screenshot)  # Clean the repository after the test
    assert added_screenshot.feature_name == feature_name
    assert added_screenshot.scenario_name == scenario_name
    assert added_screenshot.encoded_image
