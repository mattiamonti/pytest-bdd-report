from pytest_bdd import then, parsers
from playwright.sync_api import Page, expect
from tests.bdd.elements.feature_pom import FeaturePOM
import pytest


@then(parsers.cfparse("the feature '{name}' should be visible"))
def feature_should_be_visible(page: Page, name: str):
    feature = FeaturePOM(page, name)
    feature.should_be_visible()


@then(parsers.parse("the feature '{name}' should have description '{description}'"))
def feature_should_have_description(page: Page, name: str, description: str):
    feature = FeaturePOM(page, name)
    feature.should_have_description(f"Description: {description}")


@then(parsers.parse("the feature '{name}' should have path '{path}'"))
def feature_should_have_description(page: Page, name: str, path: str):
    feature = FeaturePOM(page, name)
    feature.should_have_path(path)


@then(parsers.parse("the feature '{name}' duration should not be zero"))
def feature_duration(page: Page, name: str):
    feature = FeaturePOM(page, name)
    duration = feature.get_duration()
    assert duration > 0.0


@then(
    parsers.parse(
        "the feature '{name}' badge should have {number:d} {scenario_type} scenarios"
    )
)
def feature_badge(page: Page, name: str, scenario_type: str, number: int):
    feature = FeaturePOM(page, name)
    if number <= 0:
        expect(
            feature.get().get_by_title(f"Number of test {scenario_type}")
        ).not_to_be_visible()
    else:
        badge = feature.get_scenario_badge(scenario_type)
        assert badge == number
