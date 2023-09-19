from pytest_bdd_report.components.scenario import Scenario
from pytest_bdd_report.components.step import Step
from pytest_bdd_report.report import Report
from pytest_bdd_report.components.feature import Feature
from pytest_bdd_report.summary.summary_generator import SummaryGenerator
import pytest


@pytest.fixture
def mock_report():
    report = Report("", [])
    feature = Feature(
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
    feature.total_tests = 2
    feature.passed_tests = 2
    report.add_feature(feature)

    return report


@pytest.fixture
def mock_report_failed():
    report = Report("", [])
    feature = Feature(
        id="",
        name="test feature",
        line=0,
        description="",
        tags=[],
        uri="",
        duration=0.000002,
        status="failed",
        scenarios=[
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
                        status="passed",
                        duration=1000,
                    )
                ],
            ),
        ],
    )
    feature.total_tests = 2
    feature.passed_tests = 1
    feature.failed_tests = 1
    report.add_feature(feature)

    return report


@pytest.fixture
def mock_report_long():
    report = Report("", [])
    feature = Feature(
        id="",
        name="test feature",
        line=0,
        description="",
        tags=[],
        uri="",
        duration=0.000002,
        status="failed",
        scenarios=[
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
                        status="passed",
                        duration=1000,
                    )
                ],
            ),
        ],
    )
    feature.total_tests = 2
    feature.passed_tests = 1
    feature.failed_tests = 1
    report.add_feature(feature)

    feature1 = Feature(
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
    )
    feature1.total_tests = 1
    feature1.passed_tests = 1
    report.add_feature(feature1)
    return report


def test_summary_test_statistics(mock_report):
    summary_generator = SummaryGenerator()
    summary = summary_generator.populate_summary(mock_report)
    assert summary.total_test == 2
    assert summary.test_passed == 2
    assert summary.test_failed == 0
    assert summary.test_skipped == 0


def test_summary_total_duration(mock_report):
    summary_generator = SummaryGenerator()
    summary = summary_generator.populate_summary(mock_report)
    assert summary.total_duration == 0.000002


def test_summary_test_statistics_failed(mock_report_failed):
    summary_generator = SummaryGenerator()
    summary = summary_generator.populate_summary(mock_report_failed)
    assert summary.total_test == 2
    assert summary.test_passed == 1
    assert summary.test_failed == 1
    assert summary.test_skipped == 0


def test_summary_long_report_statistics(mock_report_long):
    summary_generator = SummaryGenerator()
    summary = summary_generator.populate_summary(mock_report_long)
    assert summary.total_test == 3
    assert summary.test_passed == 2
    assert summary.test_failed == 1
    assert summary.test_skipped == 0


def test_summary_long_report_duration(mock_report_long):
    summary_generator = SummaryGenerator()
    summary = summary_generator.populate_summary(mock_report_long)
    assert summary.total_duration == 0.000003
