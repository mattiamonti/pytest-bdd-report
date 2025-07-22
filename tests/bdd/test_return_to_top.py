import pytest
from pytest_bdd import scenarios
from tests.bdd.steps.generation_steps import *
from tests.bdd.steps.common_steps import *
from tests.bdd.steps.return_to_top_steps import *

scenarios("features/return_to_top.feature")