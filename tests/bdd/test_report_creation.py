import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from pathlib import Path
from playwright.sync_api import Page
import os
from datetime import datetime
from tests.bdd.generator.bdd_generator import (
    BDDTestBuilder,
    BDDFeature,
    BDDScenario,
    create_passed_step,
    create_failed_step,
    create_skipped_step,
)

scenarios("features/report_creation.feature")

@pytest.fixture
def builder() -> BDDTestBuilder:
    return BDDTestBuilder("generated_tests")


@given(parsers.parse("a test builder with {feature:d} feature"))
def setup_features(builder, feature, cleanup_bdd_generated):
    builder.features.clear()  # clear previous features
    for i in range(feature):
        builder.add_feature(BDDFeature(f"Feature {i+1}"))


@given(parsers.parse("{count:d} passed scenarios"))
def add_passed_scenarios(builder, count):
    for i in range(count):
        scenario = BDDScenario(f"Scenario Passed {i+1}")
        scenario.add_step(create_passed_step("step passed"))
        builder.features[-1].add_scenario(scenario)


@given(parsers.parse("{count:d} failed scenarios"))
def add_failed_scenarios(builder, count):
    for i in range(count):
        scenario = BDDScenario(f"Scenario Failed {i+1}")
        scenario.add_step(create_passed_step("step passed"))
        scenario.add_step(create_failed_step("step fails"))
        builder.features[-1].add_scenario(scenario)


@given(parsers.parse("{count:d} skipped scenarios"))
def add_skipped_scenarios(builder, count):
    for i in range(count):
        scenario = BDDScenario(f"Scenario Skipped {i+1}")
        scenario.add_step(create_skipped_step("step skipped"))
        builder.features[-1].add_scenario(scenario)


@when("I generate the report")
def generate_report(builder):
    builder.build()
    test_dir = builder.output_dir
    os.system(f"pytest --bdd-report=generated_report.html {test_dir}/")


@then(parsers.parse("the report should have {expected:d} feature"))
def check_feature_in_report(page: Page, expected):
    page.goto("file://" + str(Path("generated_report.html").resolve()))
    assert page.locator(".feature").count() == expected


@then(parsers.parse("the report should have {expected:d} scenarios"))
def check_scenarios_count(page: Page, expected):
    page.goto("file://" + str(Path("generated_report.html").resolve()))
    assert page.locator(".scenario").count() == expected


@then(parsers.parse("the report should have {expected:d} passed scenarios"))
def check_passed(page: Page, expected):
    assert page.locator(".scenario-passed").count() == expected


@then(parsers.parse("the report should have {expected:d} failed scenarios"))
def check_failed(page: Page, expected):
    assert page.locator(".scenario-failed").count() == expected


@then(parsers.parse("the report should have {expected:d} skipped scenarios"))
def check_skipped(page: Page, expected):
    assert page.locator(".scenario-skipped").count() == expected

@given(parsers.parse("a test builder with a feature named '{feature_name}'"))
def setup_features(builder, feature_name:str, cleanup_bdd_generated):
    #builder.features.clear()  # clear previous features
    builder.add_feature(BDDFeature(feature_name))

@given(parsers.parse("A {type} scenario named '{scenario_name}' for the feature '{feature_name}'"))
def add_passed_scenarios(builder, type:str, scenario_name:str, feature_name:str):
    assert type in ["passed", "failed", "skipped"], f"Called with unsupported scenario type {type}"
    scenario = BDDScenario(scenario_name)
    if type == "failed":
        scenario.add_step(create_failed_step("step failed"))
    elif type == "skipped":
        scenario.add_step(create_passed_step("step passed"))
        scenario.add_step(create_skipped_step("step skipped"))
    else:
        scenario.add_step(create_passed_step("step passed"))

    for feature in builder.features:
        if feature.name == feature_name:
            feature.add_scenario(scenario)

@given(parsers.parse("{count:d} passed scenarios for the feature '{feature_name}'"))
def add_passed_scenarios(builder, count:int, feature_name:str):
    correct_feature = None
    for feature in builder.features:
        if feature.name == feature_name:
            correct_feature = feature

    for i in range(count):
        scenario = BDDScenario(f"Passing {i+1} {datetime.now().ctime()}")
        scenario.add_step(create_passed_step("step passed"))
        if correct_feature is not None: feature.add_scenario(scenario)

@given("I build the feature")
def build_feature(builder):
    builder.build()

@when("I create the report")
def generate_report(builder):
    test_dir = builder.output_dir
    os.system(f"pytest --bdd-report=generated_report.html {test_dir}/")