from pytest_bdd_report.components.scenario import Scenario
from pytest_bdd_report.components.step import Step
from pytest_bdd_report.report import Report
from pytest_bdd_report.components.feature import Feature
from pytest_bdd_report.summary.summary_generator import SummaryGenerator

mock_report_passed = Report(
    "",
    [
        Feature(
            id="",
            name="test feature",
            line=0,
            description="",
            tags=[],
            uri="",
            duration=0.000002,
            scenarios=[
                Scenario(
                    id="",
                    name="test scenario",
                    line=0,
                    description="",
                    tags=[],
                    duration=0.000001,
                    steps=[
                        Step(
                            keyword="Given",
                            name="test given",
                            line=0,
                            status="passed",
                            duration=1000,
                        )
                    ],
                ),
                Scenario(
                    id="",
                    name="test scenario",
                    line=0,
                    description="",
                    tags=[],
                    duration=0.000001,
                    status="passed",
                    steps=[
                        Step(
                            keyword="Given",
                            name="test given",
                            line=0,
                            status="passed",
                            duration=1000,
                        )
                    ],
                ),
            ],
        )
    ],
)


mock_report_failed = Report(
    "",
    [
        Feature(
            id="",
            name="test feature",
            line=0,
            description="",
            tags=[],
            uri="",
            duration=0.000002,
            scenarios=[
                Scenario(
                    id="",
                    name="test scenario",
                    line=0,
                    description="",
                    tags=[],
                    duration=0.000001,
                    steps=[
                        Step(
                            keyword="Given",
                            name="test given",
                            line=0,
                            status="passed",
                            duration=1000,
                        )
                    ],
                ),
                Scenario(
                    id="",
                    name="test scenario",
                    line=0,
                    description="",
                    tags=[],
                    duration=0.000001,
                    status="failed",
                    steps=[
                        Step(
                            keyword="Given",
                            name="test given",
                            line=0,
                            status="failed",
                            duration=1000,
                        )
                    ],
                ),
            ],
        )
    ],
)


mock_report_long = Report(
    "",
    [
        Feature(
            id="",
            name="test feature",
            line=0,
            description="",
            tags=[],
            uri="",
            duration=0.000003,
            status="failed",
            scenarios=[
                Scenario(
                    id="",
                    name="test scenario",
                    line=0,
                    description="",
                    tags=[],
                    duration=0.000001,
                    steps=[
                        Step(
                            keyword="Given",
                            name="test given",
                            line=0,
                            status="passed",
                            duration=1000,
                        )
                    ],
                ),
                Scenario(
                    id="",
                    name="test scenario",
                    line=0,
                    description="",
                    tags=[],
                    duration=0.000002,
                    status="failed",
                    steps=[
                        Step(
                            keyword="Given",
                            name="test given",
                            line=0,
                            status="passed",
                            duration=1000,
                        ),
                        Step(
                            keyword="Then",
                            name="test then",
                            line=0,
                            status="failed",
                            duration=1000,
                        ),
                    ],
                ),
            ],
        ),
        Feature(
            id="",
            name="test feature",
            line=0,
            description="",
            tags=[],
            uri="",
            duration=0.000001,
            scenarios=[
                Scenario(
                    id="",
                    name="test scenario",
                    line=0,
                    description="",
                    tags=[],
                    duration=0.000001,
                    steps=[
                        Step(
                            keyword="Given",
                            name="test given",
                            line=0,
                            status="passed",
                            duration=1000,
                        )
                    ],
                ),
            ],
        ),
    ],
)


def test_summary_test_statistics():
    summary_generator = SummaryGenerator()
    summary = summary_generator.populate_summary(mock_report_passed)
    assert summary.total_test == 2
    assert summary.test_passed == 2
    assert summary.test_failed == 0
    assert summary.test_skipped == 0


def test_summary_total_duration():
    summary_generator = SummaryGenerator()
    summary = summary_generator.populate_summary(mock_report_passed)
    assert summary.total_duration == 0.000002


def test_summary_test_statistics_failed():
    summary_generator = SummaryGenerator()
    summary = summary_generator.populate_summary(mock_report_failed)
    assert summary.total_test == 2
    assert summary.test_passed == 1
    assert summary.test_failed == 1
    assert summary.test_skipped == 0


def test_summary_long_report_statistics():
    summary_generator = SummaryGenerator()
    summary = summary_generator.populate_summary(mock_report_long)
    assert summary.total_test == 3
    assert summary.test_passed == 2
    assert summary.test_failed == 1
    assert summary.test_skipped == 0


def test_summary_long_report_duration():
    summary_generator = SummaryGenerator()
    summary = summary_generator.populate_summary(mock_report_long)
    assert summary.total_duration == 0.000004
