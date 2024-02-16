import pytest

from src.pytest_bdd_report.components.feature import Feature
from src.pytest_bdd_report.components.scenario import Scenario
from src.pytest_bdd_report.components.step import Step
from src.pytest_bdd_report.interfaces import ILoader
from src.pytest_bdd_report.report import ReportBuilder
from src.pytest_bdd_report.report_composer import ReportComposer


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


class MockLoader(ILoader):
    def __init__(self, path: str):
        super().__init__(path)

    def load(self) -> list[dict]:
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


def test_report_creation(mock_data):
    report_generator = ReportComposer(MockLoader(""), ReportBuilder(""))
    report = report_generator.create_report()
    expected_feature = Feature(
        id="tests/../features/calculator.feature",
        name="Calcolatrice",
        line=1,
        description="",
        tags=[],
        uri="tests/../features/calculator.feature",
        scenarios=[
            Scenario(
                id="test_sum",
                name="Somma di un numero",
                line=2,
                description="",
                tags=[],
                steps=[Step("Given", "I have a calculator", 3, "passed", 23040)],
                duration=0.00002304,
            )
        ],
        duration=0.00002304,
    )
    expected_feature.set_total_tests(1)
    expected_feature.set_passed_tests(1)
    assert report.features == [expected_feature]
