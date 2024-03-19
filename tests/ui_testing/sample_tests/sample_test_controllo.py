from pytest_bdd import scenario, given, when, then, parsers
import pytest
import time


@scenario('../sample_features/controllo.feature', 'Startup')
def test_accensione():
    pass


@pytest.mark.skip(reason="no way of currently testing this")
@scenario('../sample_features/controllo.feature', 'Shutdown')
def test_spegnimento():
    pass

@pytest.mark.skip(reason="no way of currently testing this")
@scenario('../sample_features/controllo.feature', 'Activation')
def test_attivazione():
    pass

@pytest.fixture
@given("I need a calculator")
def i_need_a_calculator():
    return True


@when("I press the on button")
def enter_number(i_need_a_calculator):
    time.sleep(0.001)
    assert True


@then("The calculator is ready")
def result_should_be(i_need_a_calculator):
    assert True


@pytest.fixture
@given("I have a calculator")
def i_have_a_calculator():
    return True

@when("I press the off button")
def press_off():
    assert False


@then("The calculator is off")
def off_calculator():
    assert True
