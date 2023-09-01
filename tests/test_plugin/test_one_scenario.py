import json
import pytest
import textwrap


# fixture for an example test that pass
@pytest.fixture()
def sample_test_pass(testdir):
    testdir.makefile(
        ".feature",
        scenario=textwrap.dedent(
            """\
            Feature: Testing
                Scenario: Test scenario
                    Given I have a scenario
                    Then Should be created
            """
        ),
    )

    testdir.makepyfile(
        textwrap.dedent(
            """\
        import pytest
        from pytest_bdd import given, then, scenario

        @scenario("scenario.feature", "Test scenario")
        def test_scenario():
            pass

        @given("I have a scenario")
        def _():
            pass

        @then('Should be created')
        def _():
            assert True

        """
        )
    )

    return testdir


# fixture for an example test that fail
@pytest.fixture
def sample_test_fail(testdir):
    testdir.makefile(
        ".feature",
        scenario=textwrap.dedent(
            """\
            Feature: Testing
                Scenario: Test scenario
                    Given I have a scenario
                    Then Should be created
            """
        ),
    )

    testdir.makepyfile(
        textwrap.dedent(
            """\
        import pytest
        from pytest_bdd import given, then, scenario

        @scenario("scenario.feature", "Test scenario")
        def test_scenario():
            pass

        @given("I have a scenario")
        def _():
            pass

        @then('Should be created')
        def _():
            assert False

        """
        )
    )

    return testdir


def test_json_content_scenario_pass(sample_test_pass):
    sample_test_pass.runpytest("--bdd-json")

    with open(str(sample_test_pass.tmpdir / "session_finish_results.json")) as f:
        data = json.load(f)

    assert data[0]["nodeid"] != ""
    assert data[0]["feature"] == "Testing"
    assert data[0]["scenario"] == "Test scenario"
    assert data[0]["outcome"] == "passed"
    assert data[0]["duration"] != 0
    assert len(data[0]["steps"]) == 2


def test_json_content_steps_pass(sample_test_pass):
    sample_test_pass.runpytest("--bdd-json")

    with open(str(sample_test_pass.tmpdir / "session_finish_results.json")) as f:
        data = json.load(f)

    assert len(data[0]["steps"]) == 2
    assert data[0]["steps"][0]["nodeid"] != ""
    assert data[0]["steps"][0]["type"] == "Given"
    assert data[0]["steps"][0]["step"] == "I have a scenario"
    assert data[0]["steps"][0]["status"] == "passed"
    assert data[0]["steps"][1]["nodeid"] != ""
    assert data[0]["steps"][1]["type"] == "Then"
    assert data[0]["steps"][1]["step"] == "Should be created"
    assert data[0]["steps"][1]["status"] == "passed"


def test_json_content_scenario_fail(sample_test_fail):
    res = sample_test_fail.runpytest("--bdd-json")

    with open(str(sample_test_fail.tmpdir / "session_finish_results.json")) as f:
        data = json.load(f)

    res.assert_outcomes(failed=1)

    assert data[0]["nodeid"] != ""
    assert data[0]["feature"] == "Testing"
    assert data[0]["scenario"] == "Test scenario"
    assert data[0]["outcome"] == "failed"
    assert data[0]["longrepr"] != ""
    assert data[0]["duration"] != 0


def test_json_content_steps_fail(sample_test_fail):
    res = sample_test_fail.runpytest("--bdd-json")

    with open(str(sample_test_fail.tmpdir / "session_finish_results.json")) as f:
        data = json.load(f)

    res.assert_outcomes(failed=1)

    assert len(data[0]["steps"]) == 2
    assert data[0]["steps"][0]["nodeid"] != ""
    assert data[0]["steps"][0]["type"] == "Given"
    assert data[0]["steps"][0]["step"] == "I have a scenario"
    assert data[0]["steps"][0]["status"] == "passed"
    assert data[0]["steps"][1]["nodeid"] != ""
    assert data[0]["steps"][1]["type"] == "Then"
    assert data[0]["steps"][1]["step"] == "Should be created"
    assert data[0]["steps"][1]["status"] == "failed"
    assert data[0]["steps"][1]["exception"] != ""
