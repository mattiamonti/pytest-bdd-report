from pytest_bdd import scenario, given, when, then, parsers
import pytest


@scenario("../sample_features/calculator.feature", "Sum of a number")
def test_sum():
    pass


@scenario("../sample_features/calculator.feature", "Sum of two numbers")
def test_sum_2():
    pass


@scenario("../sample_features/calculator.feature", "Sum of negative numbers")
def test_sum_3():
    pass


@pytest.fixture
@given("I have a calculator")
def i_have_a_calculator():
    calculator = Calculator()
    return calculator


@when(parsers.cfparse("I enter the number {number} into the calculator"))
def enter_number(i_have_a_calculator, number):
    i_have_a_calculator.enter_number(number)


@when("I press the add button")
def press_add_button(i_have_a_calculator):
    i_have_a_calculator.press_add()


@then(parsers.cfparse("The result should be {result} on the screen"))
def result_should_be(i_have_a_calculator, result):
    assert i_have_a_calculator.result == int(result)


class Calculator:
    def __init__(self):
        self.result = 0
        self.e1 = 0
        self.e2 = 0

    def enter_number(self, number):
        if self.e1 == 0:
            self.e1 = int(number)
        else:
            self.e2 = int(number)

    def press_add(self):
        # Implementa la logica per la somma
        self.result = self.e1 + self.e2

    def get_result(self):
        return self.result
