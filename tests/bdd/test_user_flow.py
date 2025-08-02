import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page, Locator, expect
from tests.bdd.steps.generation_steps import *
from tests.bdd.steps.common_steps import *
from tests.bdd.steps.feature_statistic_table_steps import *
from tests.bdd.steps.feature_steps import *
from tests.bdd.steps.feature_table_steps import *
from tests.bdd.steps.filter_steps import *
from tests.bdd.steps.modal_steps import *
from tests.bdd.steps.scenario_steps import *
from tests.bdd.steps.return_to_top_steps import *


scenarios("features/user_flow.feature")
