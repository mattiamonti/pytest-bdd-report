
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
from tests.bdd.elements.feature_pom import FeaturePOM
from tests.bdd.elements.scenario_pom import ScenarioPOM

@pytest.fixture
def feature(page: Page) -> FeaturePOM:
    return FeaturePOM(page)

@pytest.fixture
def scenario(page: Page):
    return ScenarioPOM(page)

@pytest.fixture
def builder() -> BDDTestBuilder:
    return BDDTestBuilder("generated_tests")

@given(parsers.parse("a test builder with a feature named '{feature_name}'"))
def setup_features(builder, feature_name:str, cleanup_bdd_generated):
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

@given(parsers.parse("{count:d} {type} scenarios for the feature '{feature_name}'"))
def add_passed_scenarios(builder, count:int, type:str, feature_name:str, get_uuid):
    assert type in ["passed", "failed", "skipped"], f"Called with unsupported scenario type {type}"
    correct_feature = None
    for feature in builder.features:
        if feature.name == feature_name:
            correct_feature = feature

    for i in range(count):
        scenario = BDDScenario(f"Passing {i+1} {get_uuid()}")
        if type == "failed":
            scenario.add_step(create_failed_step("step failed"))
        elif type == "skipped":
            scenario.add_step(create_passed_step("step passed"))
            scenario.add_step(create_skipped_step("step skipped"))
        else:
            scenario.add_step(create_passed_step("step passed"))
        if correct_feature is not None: feature.add_scenario(scenario)

@given("I build the feature")
def build_feature(builder):
    builder.build()

@when("I create the report")
def generate_report(builder):
    test_dir = builder.output_dir
    os.system(f"pytest --bdd-report=generated_report.html {test_dir}/")

@when("I open the report")
def check_feature_in_report(page: Page):
    page.goto("file://" + str(Path("generated_report.html").resolve()))



@then(parsers.parse("the report should have {expected:d} feature"))
def check_feature_in_report(feature: FeaturePOM, expected:int):
    assert feature.get_all().count() == expected

@then(parsers.parse("the report should have {expected:d} scenarios"))
def check_scenarios_count(scenario: ScenarioPOM, expected:int):
    assert scenario.get_all().count() == expected

@then(parsers.parse("the report should have {expected:d} {type} scenarios"))
def check_passed(scenario: ScenarioPOM, expected: int, type:str):
    #assert page.locator(".scenario-passed").count() == expected
    assert type in ["passed", "failed", "skipped"], f"Called with unsupported scenario type {type}"
    if type == "failed":
        assert scenario.get_failed().count() == expected
    elif type == "skipped":
        assert scenario.get_skipped().count() == expected
    else:
        assert scenario.get_passed().count() == expected