import pytest
from pytest_bdd import scenarios
from tests.bdd.steps.generation_steps import *

scenarios("features/report_creation.feature")
