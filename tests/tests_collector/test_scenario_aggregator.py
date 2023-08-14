import pytest
from collector.scenario_aggregator import ScenarioAggregator


@pytest.fixture
def mock_steps_information():
    return [
        {
            "feature": "Feature 1",
            "scenario": "Scenario A",
            "type": "Given",
            "step": "Some given step",
            "status": "passed",
            "nodeid": "node1",
            "exception": "",
        },
        {
            "feature": "Feature 1",
            "scenario": "Scenario A",
            "type": "When",
            "step": "Some when step",
            "status": "passed",
            "nodeid": "node2",
            "exception": "",
        },
        {
            "feature": "Feature 1",
            "scenario": "Scenario A",
            "type": "Then",
            "step": "Some then step",
            "status": "passed",
            "nodeid": "node3",
            "exception": "",
        },
        {
            "feature": "Feature 1",
            "scenario": "Scenario B",
            "type": "Given",
            "step": "Some given step",
            "status": "passed",
            "nodeid": "node1",
            "exception": "",
        },
        {
            "feature": "Feature 1",
            "scenario": "Scenario B",
            "type": "When",
            "step": "Some when step",
            "status": "passed",
            "nodeid": "node2",
            "exception": "",
        },
    ]


def test_aggregate_steps_into_scenario(mock_steps_information):
    aggregator = ScenarioAggregator()

    aggregated_results = aggregator.aggregate_steps_into_scenario(
        mock_steps_information
    )

    # Test if the scenario is aggregated correctly
    assert "Feature 1 - Scenario A" in aggregated_results
    assert len(aggregated_results["Feature 1 - Scenario A"]["steps"]) == 3
    assert len(aggregated_results["Feature 1 - Scenario B"]["steps"]) == 2


def test_aggregated_steps_content(mock_steps_information):
    aggregator = ScenarioAggregator()

    aggregated_results = aggregator.aggregate_steps_into_scenario(
        mock_steps_information
    )

    scenario_a_steps = aggregated_results["Feature 1 - Scenario A"]["steps"]

    assert (
        scenario_a_steps[0]["type"] == "Given"
        and scenario_a_steps[0]["nodeid"] == "node1"
    )
    assert (
        scenario_a_steps[1]["type"] == "When"
        and scenario_a_steps[1]["nodeid"] == "node2"
    )
    assert (
        scenario_a_steps[2]["type"] == "Then"
        and scenario_a_steps[2]["nodeid"] == "node3"
    )
