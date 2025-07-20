import pytest
from pytest_bdd import given, scenario

@given("lo step è passato")
def lo_step_è_passato(request):
        pass

@given("lo step è fallito")
def lo_step_è_fallito(request):
        raise AssertionError("Step failed intentionally")


@scenario("feature_1.feature", "Failed 1")
def test_failed_1():
    pass

@scenario("feature_1.feature", "Failed 2")
def test_failed_2():
    pass

@scenario("feature_1.feature", "Failed 3")
def test_failed_3():
    pass