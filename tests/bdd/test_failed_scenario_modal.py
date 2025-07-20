from pytest_bdd import scenarios
from tests.bdd.steps.setup_steps import *
from tests.bdd.steps.common_steps import *
from tests.bdd.steps.modal_steps import *
from tests.bdd.steps.scenario_steps import *

scenarios("features/failed_scenario_modal.feature")