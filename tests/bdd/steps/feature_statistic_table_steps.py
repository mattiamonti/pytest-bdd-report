from pytest_bdd import then, parsers
from playwright.sync_api import Page, expect
from tests.bdd.elements.feature_statistic_table_pom import FeatureStatisticTablePOM
import pytest

@then(parsers.cfparse("the feature statistic table should have a row for the feature '{feature_name}'"))
def table_should_have_row(page: Page, feature_name: str):
    table = FeatureStatisticTablePOM(page)
    row = table.get_row(feature_name)
    expect(row).to_be_visible()
    expect(row).not_to_be_hidden()

@then(parsers.cfparse("the feature statistic table row for the feature '{feature_name}' should have {value} in column '{column_name}'"))
def has_column(page: Page, feature_name: str, value: str, column_name: str):
    table = FeatureStatisticTablePOM(page)
    row = table.get_row(feature_name)
    column = table.get_column(column_name)
    expect(column).not_to_be_hidden()
    if column_name == "Duration":
        match value:
            case ">0": assert table.get_column_duration() > 0.0
            case "=0": assert table.get_column_duration() == 0.0
    else:
        expect(column).to_contain_text(value)

