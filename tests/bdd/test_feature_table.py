from pytest_bdd import scenarios
from tests.bdd.steps.setup_steps import *
from tests.bdd.steps.common_steps import *
from tests.bdd.steps.feature_steps import *
from tests.bdd.steps.feature_table_steps import *

scenarios("features/feature_table.feature")