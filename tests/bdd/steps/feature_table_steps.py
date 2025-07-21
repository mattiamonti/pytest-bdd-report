from pytest_bdd import then, parsers, when
from playwright.sync_api import Page, expect
from tests.bdd.elements.feature_table_pom import FeatureTablePOM
import pytest
import time


@pytest.fixture
def feature_table(page: Page):
    return FeatureTablePOM(page)


@when(parsers.cfparse("I click on the feature link '{name}'"))
def feature_should_be_visible(feature_table: FeatureTablePOM, name: str):
    feature_table.click_feature_link(name)
