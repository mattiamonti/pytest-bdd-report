import json
import pytest
import textwrap


# fixture for an example test with multiple scenarios that pass
@pytest.fixture
def sample_multiple_scenarios_test_pass(testdir):
    testdir.makefile(
        ".feature",
        scenario=textwrap.dedent(
            """\
            Feature: Testing
                Scenario: Test scenario one
                    Given I have a scenario
                    Then Should be created

                Scenario: Test scenario two
                    Given I have a scenario
                    When I create the scenario
                    Then Should be created
            """
        ),
    )

    testdir.makepyfile(
        textwrap.dedent(
            """\
        import pytest
        from pytest_bdd import given, when, then, scenario

        @scenario("scenario.feature", "Test scenario one")
        def test_scenario_one():
            pass
        
        @scenario("scenario.feature", "Test scenario two")
        def test_scenario_two():
            pass

        @given("I have a scenario")
        def _():
            pass
            
        @when("I create the scenario")
        def _():
            pass

        @then('Should be created')
        def _():
            assert True

        """
        )
    )

    return testdir


# fixture for an example test with multiple scenarios that fail
@pytest.fixture
def sample_multiple_scenarios_test_fail(testdir):
    testdir.makefile(
        ".feature",
        scenario=textwrap.dedent(
            """\
            Feature: Testing
                Scenario: Test scenario one
                    Given I have a scenario
                    Then Should be created

                Scenario: Test scenario two
                    Given I have a scenario
                    When I create the scenario
                    Then Should be created
            """
        ),
    )

    testdir.makepyfile(
        textwrap.dedent(
            """\
        import pytest
        from pytest_bdd import given, when, then, scenario

        @scenario("scenario.feature", "Test scenario one")
        def test_scenario_one():
            pass
        
        @scenario("scenario.feature", "Test scenario two")
        def test_scenario_two():
            pass

        @given("I have a scenario")
        def _():
            pass
            
        @when("I create the scenario")
        def _():
            assert False

        @then('Should be created')
        def _():
            assert True

        """
        )
    )

    return testdir


def test_json_content_multiple_scenarios_pass(sample_multiple_scenarios_test_pass):
    sample_multiple_scenarios_test_pass.runpytest("--bdd-json")

    with open(
        str(sample_multiple_scenarios_test_pass.tmpdir / "session_finish_results.json")
    ) as f:
        data = json.load(f)

    assert len(data) == 2
    # first test
    assert data[0]["nodeid"] != ""
    assert data[0]["feature"] == "Testing"
    assert data[0]["scenario"] == "Test scenario one"
    assert data[0]["outcome"] == "passed"
    assert data[0]["duration"] != 0
    assert len(data[0]["steps"]) == 2
    # second test
    assert data[1]["nodeid"] != ""
    assert data[1]["feature"] == "Testing"
    assert data[1]["scenario"] == "Test scenario two"
    assert data[1]["outcome"] == "passed"
    assert data[1]["duration"] != 0
    assert len(data[1]["steps"]) == 3


def test_json_content_multiple_scenarios_steps_pass(
    sample_multiple_scenarios_test_pass,
):
    sample_multiple_scenarios_test_pass.runpytest("--bdd-json")

    with open(
        str(sample_multiple_scenarios_test_pass.tmpdir / "session_finish_results.json")
    ) as f:
        data = json.load(f)

    # first scenario steps
    first_steps = data[0]["steps"]
    assert first_steps[0]["type"] == "Given"
    assert first_steps[0]["status"] == "passed"
    assert first_steps[1]["type"] == "Then"
    assert first_steps[1]["status"] == "passed"
    # second scenario steps
    second_steps = data[1]["steps"]
    assert second_steps[0]["type"] == "Given"
    assert second_steps[0]["status"] == "passed"
    assert second_steps[1]["type"] == "When"
    assert second_steps[1]["status"] == "passed"
    assert second_steps[2]["type"] == "Then"
    assert second_steps[2]["status"] == "passed"


def test_json_content_multiple_scenarios_fail(sample_multiple_scenarios_test_fail):
    sample_multiple_scenarios_test_fail.runpytest("--bdd-json")

    with open(
        str(sample_multiple_scenarios_test_fail.tmpdir / "session_finish_results.json")
    ) as f:
        data = json.load(f)

    assert len(data) == 2
    # first test
    assert data[0]["nodeid"] != ""
    assert data[0]["feature"] == "Testing"
    assert data[0]["scenario"] == "Test scenario one"
    assert data[0]["outcome"] == "passed"
    assert data[0]["duration"] != 0
    assert len(data[0]["steps"]) == 2
    # second test
    assert data[1]["nodeid"] != ""
    assert data[1]["feature"] == "Testing"
    assert data[1]["scenario"] == "Test scenario two"
    assert data[1]["outcome"] == "failed"
    assert data[1]["duration"] != 0
    assert data[1]["steps"][1]["type"] == "When"
    assert data[1]["steps"][1]["step"] == "I create the scenario"
    assert data[1]["steps"][1]["status"] == "failed"


def test_json_content_multiple_scenarios_steps_fail(
    sample_multiple_scenarios_test_fail,
):
    sample_multiple_scenarios_test_fail.runpytest("--bdd-json")

    with open(
        str(sample_multiple_scenarios_test_fail.tmpdir / "session_finish_results.json")
    ) as f:
        data = json.load(f)

    # first scenario steps
    first_steps = data[0]["steps"]
    assert first_steps[0]["type"] == "Given"
    assert first_steps[0]["status"] == "passed"
    assert first_steps[1]["type"] == "Then"
    assert first_steps[1]["status"] == "passed"
    # second scenario steps
    second_steps = data[1]["steps"]
    assert second_steps[0]["type"] == "Given"
    assert second_steps[0]["status"] == "passed"
    assert second_steps[1]["type"] == "When"
    assert second_steps[1]["status"] == "failed"
