from pytest_bdd import then, parsers
from playwright.sync_api import Page, expect
from tests.bdd.elements.feature_pom import FeaturePOM
import pytest


@pytest.fixture
def feature(page: Page):
    return FeaturePOM(page)


@then(parsers.cfparse("the feature '{name}' should be visible"))
def feature_should_be_visible(feature: FeaturePOM, name: str):
    feature.should_be_visible(name)
