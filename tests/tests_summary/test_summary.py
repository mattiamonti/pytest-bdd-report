import pytest
from unittest.mock import MagicMock, patch
from summary.summary import Summary


# Mock the save_to_json function
@pytest.fixture
def mock_save_to_json(monkeypatch):
    mock_function = MagicMock()
    monkeypatch.setattr("summary.summary.save_to_json", mock_function)
    return mock_function


# Test cases for the Summary class
def test_initial_summary_values():
    summary = Summary()
    assert summary.summary == {
        "total_tests": 0,
        "passed_tests": 0,
        "failed_tests": 0,
        "skipped_tests": 0,
    }


def test_add_passed_test():
    summary = Summary()
    summary.add_passed_test()
    assert summary.summary["total_tests"] == 1
    assert summary.summary["passed_tests"] == 1


def test_add_failed_test():
    summary = Summary()
    summary.add_failed_test()
    assert summary.summary["total_tests"] == 1
    assert summary.summary["failed_tests"] == 1


def test_add_skipped_test():
    summary = Summary()
    summary.add_skipped_test()
    assert summary.summary["total_tests"] == 1
    assert summary.summary["skipped_tests"] == 1


@patch("summary.summary.save_to_json")
def test_save_to_json(mock_save_function):
    summary = Summary()
    summary.save_to_json("test_summary.json")
    mock_save_function.assert_called_once_with(
        {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "skipped_tests": 0,
        },
        "test_summary.json",
    )
