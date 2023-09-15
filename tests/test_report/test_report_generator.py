from pytest_bdd_report.components.feature import Feature
from pytest_bdd_report.components.scenario import Scenario
from pytest_bdd_report.report import Report
from pytest_bdd_report.report_generator import ReportGenerator
from pytest_bdd_report.components.step import Step


mock_data = [
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

mock_scenario = {
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
}


def test_steps_extraction():
    report = Report("", [])
    report_generator = ReportGenerator(mock_data, report)
    steps = report_generator.extract_steps(mock_scenario["steps"])
    assert steps == [Step("Given", "I have a calculator", 3, "passed", 23040)]


def test_scenario_extraction():
    report = Report("", [])
    report_generator = ReportGenerator(mock_data, report)
    scenarios = report_generator.extract_scenarios(mock_data[0]["elements"])
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


def test_feature_extraction():
    report = Report("", [])
    report_generator = ReportGenerator(mock_data, report)
    features = report_generator.extract_features()
    assert features == [
        Feature(
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
        ),
    ]


def test_report_creation():
    report = Report("", [])
    report_generator = ReportGenerator(mock_data, report)
    report_generator.create_report()
    assert report.features == [
        Feature(
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
                    duration=0.00002304
                )
            ],
            duration=0.00002304
        ),
    ]

