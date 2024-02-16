import pytest

from src.pytest_bdd_report.components.feature import Feature
from src.pytest_bdd_report.components.scenario import Scenario
from src.pytest_bdd_report.components.step import Step
from src.pytest_bdd_report.extractor import (
    StepExtractor,
    ScenarioExtractor,
    FeatureExtractor,
)


@pytest.fixture
def mock_data():
    return [
        {
            "keyword": "Feature",
            "uri": "tests/../features/calculator.feature",
            "name": "Calcolatrice",
            "id": "tests/../features/calculator.feature",
            "line": 1,
            "description": "",
            "tags": [],
            "elements": [
                {
                    "keyword": "Scenario",
                    "id": "test_sum",
                    "name": "Somma di un numero",
                    "line": 2,
                    "description": "",
                    "tags": [],
                    "type": "scenario",
                    "steps": [
                        {
                            "keyword": "Given",
                            "name": "I have a calculator",
                            "line": 3,
                            "match": {"location": ""},
                            "result": {"status": "passed", "duration": 23040},
                        },
                    ],
                },
            ],
        }
    ]


@pytest.fixture
def mock_scenario(mock_data):
    return mock_data[0]["elements"][0]


def test_steps_extraction(mock_scenario):
    steps = StepExtractor().extract_from(mock_scenario["steps"])
    assert steps == [Step("Given", "I have a calculator", 3, "passed", 23040)]


def test_scenario_extraction(mock_data):
    scenarios = ScenarioExtractor().extract_from(mock_data[0]["elements"])
    assert scenarios == [
        Scenario(
            "test_sum",
            "Somma di un numero",
            2,
            "",
            [],
            [Step("Given", "I have a calculator", 3, "passed", 23040)],
        )
    ]


def test_feature_extraction(mock_data):
    features = FeatureExtractor().extract_from(mock_data)
    expected = Feature(
        "tests/../features/calculator.feature",
        "Calcolatrice",
        1,
        "",
        [],
        "tests/../features/calculator.feature",
        [
            Scenario(
                "test_sum",
                "Somma di un numero",
                2,
                "",
                [],
                [Step("Given", "I have a calculator", 3, "passed", 23040)],
            )
        ],
    )
    expected.set_total_tests(1)
    expected.set_passed_tests(1)
    expected.set_failed_tests(0)
    expected.set_skipped_test(0)

    assert features[0] == expected


@pytest.fixture
def mock_data_with_more_features():
    return [
        {
            "keyword": "Feature",
            "uri": "tests/../features/calculator.feature",
            "name": "Calcolatrice",
            "id": "tests/../features/calculator.feature",
            "line": 1,
            "description": "",
            "tags": [],
            "elements": [
                {
                    "keyword": "Scenario",
                    "id": "test_sum",
                    "name": "Somma di un numero",
                    "line": 2,
                    "description": "",
                    "tags": [],
                    "type": "scenario",
                    "steps": [
                        {
                            "keyword": "Given",
                            "name": "I have a calculator",
                            "line": 3,
                            "match": {"location": ""},
                            "result": {"status": "passed", "duration": 23040},
                        },
                    ],
                },
                {
                    "keyword": "Scenario",
                    "id": "test_sum_2",
                    "name": "Somma di due numeri",
                    "line": 2,
                    "description": "",
                    "tags": [],
                    "type": "scenario",
                    "steps": [
                        {
                            "keyword": "Given",
                            "name": "I have a calculator",
                            "line": 3,
                            "match": {"location": ""},
                            "result": {"status": "passed", "duration": 23040},
                        },
                    ],
                },
            ],
        },
        {
            "keyword": "Feature",
            "uri": "tests/../features/calculator.feature",
            "name": "Calcolatrice 2",
            "id": "tests/../features/calculator.feature",
            "line": 1,
            "description": "",
            "tags": [],
            "elements": [
                {
                    "keyword": "Scenario",
                    "id": "test_sum",
                    "name": "Somma di un numero 2",
                    "line": 2,
                    "description": "",
                    "tags": [],
                    "type": "scenario",
                    "steps": [
                        {
                            "keyword": "Given",
                            "name": "I have a calculator",
                            "line": 3,
                            "match": {"location": ""},
                            "result": {"status": "passed", "duration": 23040},
                        },
                    ],
                },
                {
                    "keyword": "Scenario",
                    "id": "test_sum_2",
                    "name": "Somma di due numeri 2",
                    "line": 2,
                    "description": "",
                    "tags": [],
                    "type": "scenario",
                    "steps": [
                        {
                            "keyword": "Given",
                            "name": "I have a calculator",
                            "line": 3,
                            "match": {"location": ""},
                            "result": {"status": "passed", "duration": 23040},
                        },
                    ],
                },
            ],
        },
    ]


def test_scenario_extraction_with_more(mock_data_with_more_features):
    scenarios = ScenarioExtractor().extract_from(
        mock_data_with_more_features[0]["elements"]
    )
    assert scenarios == [
        Scenario(
            "test_sum",
            "Somma di un numero",
            2,
            "",
            [],
            [Step("Given", "I have a calculator", 3, "passed", 23040)],
        ),
        Scenario(
            "test_sum_2",
            "Somma di due numeri",
            2,
            "",
            [],
            [Step("Given", "I have a calculator", 3, "passed", 23040)],
        ),
    ]


def test_feature_extraction_with_more(mock_data_with_more_features):
    features = FeatureExtractor().extract_from(mock_data_with_more_features)
    assert len(features) == 2
    expected_1 = Feature(
        "tests/../features/calculator.feature",
        "Calcolatrice",
        1,
        "",
        [],
        "tests/../features/calculator.feature",
        [
            Scenario(
                "test_sum",
                "Somma di un numero",
                2,
                "",
                [],
                [Step("Given", "I have a calculator", 3, "passed", 23040)],
            ),
            Scenario(
                "test_sum_2",
                "Somma di due numeri",
                2,
                "",
                [],
                [Step("Given", "I have a calculator", 3, "passed", 23040)],
            ),
        ],
    )
    expected_1.set_total_tests(2)
    expected_1.set_passed_tests(2)
    expected_1.set_failed_tests(0)
    expected_1.set_skipped_test(0)

    expected_2 = Feature(
        "tests/../features/calculator.feature",
        "Calcolatrice 2",
        1,
        "",
        [],
        "tests/../features/calculator.feature",
        [
            Scenario(
                "test_sum",
                "Somma di un numero 2",
                2,
                "",
                [],
                [Step("Given", "I have a calculator", 3, "passed", 23040)],
            ),
            Scenario(
                "test_sum_2",
                "Somma di due numeri 2",
                2,
                "",
                [],
                [Step("Given", "I have a calculator", 3, "passed", 23040)],
            ),
        ],
    )
    expected_2.set_total_tests(2)
    expected_2.set_passed_tests(2)
    expected_2.set_failed_tests(0)
    expected_2.set_skipped_test(0)

    assert features == [expected_1, expected_2]
