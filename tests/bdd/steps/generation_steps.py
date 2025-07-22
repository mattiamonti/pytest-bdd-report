from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page, expect
import pytest
import os
from pathlib import Path
from tests.bdd.generator.bdd_generator import (
    BDDTestBuilder,
    BDDFeature,
    BDDScenario,
    create_passed_step,
    create_failed_step,
    create_skipped_step,
)
from tests.bdd.elements.report_pom import ReportPOM


@pytest.fixture
def report(page: Page) -> ReportPOM:
    return ReportPOM(page)


@pytest.fixture
def builder() -> BDDTestBuilder:
    return BDDTestBuilder("generated_tests")


@given(parsers.parse("a test builder with a feature named '{feature_name}'"))
def setup_features(builder, feature_name: str, cleanup_bdd_generated):
    builder.add_feature(BDDFeature(feature_name))


@given(
    parsers.parse(
        "the feature '{feature_name}' has the description '{feature_description}'"
    )
)
def add_feature_description(builder, feature_name: str, feature_description: str):
    for feature in builder.features:
        if feature.name == feature_name:
            feature.add_description(feature_description)


@given(
    parsers.parse(
        "A {type} scenario named '{scenario_name}' for the feature '{feature_name}'"
    )
)
def add_passed_scenarios(builder, type: str, scenario_name: str, feature_name: str):
    scenario = BDDScenario(scenario_name)
    scenario = _add_step_to_scenario(type, scenario)

    for feature in builder.features:
        if feature.name == feature_name:
            feature.add_scenario(scenario)


@given(parsers.parse("{count:d} {type} scenarios for the feature '{feature_name}'"))
def add_multiple_passed_scenarios(
    builder, count: int, type: str, feature_name: str, get_uuid
):
    correct_feature = None
    for feature in builder.features:
        if feature.name == feature_name:
            correct_feature = feature

    for i in range(count):
        scenario = BDDScenario(f"Passing {i+1} {get_uuid()}")
        scenario = _add_step_to_scenario(type, scenario)
        if correct_feature is not None:
            correct_feature.add_scenario(scenario)


def _add_step_to_scenario(scenario_type: str, scenario: BDDScenario) -> BDDScenario:
    assert scenario_type in ["passed", "failed", "skipped"]
    if scenario_type == "failed":
        scenario.add_step(create_failed_step("step failed"))
    elif scenario_type == "skipped":
        scenario.add_step(create_passed_step("step passed"))
        scenario.add_step(create_skipped_step("step skipped"))
    else:
        scenario.add_step(create_passed_step("step passed"))
    return scenario


@given("I build the feature")
def build_feature(builder):
    builder.build()


@when("I create the report")
def generate_report(builder):
    test_dir = builder.output_dir
    os.system(f"pytest --bdd-report=generated_report.html {test_dir}/")


@when("I open the report")
def open_the_report(page: Page):
    page.goto("file://" + str(Path("generated_report.html").resolve()))


@then(parsers.parse("the report should have {expected:d} feature"))
def check_feature_in_report(report: ReportPOM, expected: int):
    assert report.get_all_features().count() == expected


@then(parsers.parse("the report should have {expected:d} scenarios"))
def check_scenarios_count(report: ReportPOM, expected: int):
    assert report.get_all_scenarios().count() == expected


@then(parsers.parse("the report should have {expected:d} {type} scenarios"))
def check_passed(report: ReportPOM, expected: int, type: str):
    assert type in ["passed", "failed", "skipped"]
    if type == "failed":
        assert report.get_failed_scenarios().count() == expected
    elif type == "skipped":
        assert report.get_skipped_scenarios().count() == expected
    else:
        assert report.get_passed_scenarios().count() == expected
