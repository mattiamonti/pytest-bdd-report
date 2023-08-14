import pytest
from collector.scenario_result_merger import (
    ScenarioAndResultMerger,
    LengthMismatchError,
)


@pytest.fixture
def mock_aggregated_scenarios():
    return {
        "Feature 1 - Scenario A": {
            "feature": "Feature 1",
            "scenario": "Scenario A",
            "steps": ["Step 1", "Step 2", "Step 3"],
        }
    }


@pytest.fixture
def mock_tests_results():
    return [
        {
            "nodeid": "node1",
            "duration": 0.5,
            "outcome": "passed",
            "longrepr": "Test passed successfully.",
        },
    ]


def test_merge_scenario_and_result_length(
    mock_aggregated_scenarios, mock_tests_results
):
    merger = ScenarioAndResultMerger()
    merged_results = merger.merge_scenario_and_result(
        mock_aggregated_scenarios, mock_tests_results
    )

    assert len(merged_results) == len(mock_aggregated_scenarios.values())
    assert len(merged_results) == len(mock_tests_results)
    assert merged_results[0]["feature"] == "Feature 1"
    assert merged_results[0]["scenario"] == "Scenario A"


def test_merge_scenario_and_result_content(
    mock_aggregated_scenarios, mock_tests_results
):
    merger = ScenarioAndResultMerger()
    merged_results = merger.merge_scenario_and_result(
        mock_aggregated_scenarios, mock_tests_results
    )

    assert merged_results[0]["feature"] == "Feature 1"
    assert merged_results[0]["scenario"] == "Scenario A"
    assert merged_results[0]["nodeid"] == "node1"
    assert merged_results[0]["outcome"] == "passed"
    assert merged_results[0]["duration"] == 0.5


def test_merge_scenario_and_result_mismatch(mock_aggregated_scenarios):
    # tests_results too longo to merge
    mock_tests_results = [
        {
            "nodeid": "node1",
            "duration": 0.5,
            "outcome": "passed",
            "longrepr": "Test passed successfully.",
        },
        {
            "nodeid": "node2",
            "duration": 0.5,
            "outcome": "failed",
            "longrepr": "Test failed",
        },
    ]

    merger = ScenarioAndResultMerger()

    with pytest.raises(LengthMismatchError):
        merger.merge_scenario_and_result(mock_aggregated_scenarios, mock_tests_results)
