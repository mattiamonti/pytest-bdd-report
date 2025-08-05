import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page, Locator, expect
from tests.bdd.steps.generation_steps import *
from tests.bdd.steps.common_steps import *
from tests.bdd.steps.feature_statistic_table_steps import *


scenarios("features/feature_statistic_table.feature")
