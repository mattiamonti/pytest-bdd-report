from pytest_bdd import scenarios
# Importa gli step definiti altrove
from tests.bdd.steps.setup_steps import *
from tests.bdd.steps.common_steps import *
from tests.bdd.steps.modal_steps import *
from tests.bdd.steps.scenario_steps import *

scenarios("features/scenario_modal.feature")