import json
import pytest
import textwrap


def test_arguments_in_help(testdir):
    res = testdir.runpytest("--help")
    res.stdout.fnmatch_lines(
        [
            "*bdd-json*",
            "*report*",
        ]
    )


def test_json_message_in_stdout(testdir):
    res = testdir.runpytest("--bdd-json")
    res.stdout.fnmatch_lines(
        [
            "*JSON with the tests result created successfully*",
        ]
    )


def test_report_message_in_stdout(testdir):
    arg = "test"
    res = testdir.runpytest(f"--report={arg}")
    res.stdout.fnmatch_lines(
        [
            f"*Report created at: {arg}*.html*",
        ]
    )


def test_report_message_in_stdout_with_html(testdir):
    arg = "test.html"
    res = testdir.runpytest(f"--report={arg}")
    res.stdout.fnmatch_lines(
        [
            f"*Report created at: {arg}*",
        ]
    )


# fixture for an example test that pass
@pytest.fixture()
def sample_test(testdir):
    testdir.makefile(
        ".feature",
        scenario=textwrap.dedent(
            """\
            Feature: Testing
                Scenario: Test scenario
                    Given I have a scenario
                    When I start the test
                    And I know it will fails
                    Then It fails
            """
        ),
    )

    testdir.makepyfile(
        textwrap.dedent(
            """\
        import pytest
        from pytest_bdd import given, when, then, scenario

        @scenario("scenario.feature", "Test scenario")
        def test_scenario():
            pass

        @given("I have a scenario")
        def _():
            pass
            
        @when("I start the test")
        def _():
            pass
        
        @when("I know it will fails")
        def _():
            pass

        @then('It fails')
        def _():
            assert False

        """
        )
    )

    return testdir


def test_create_json(sample_test):
    sample_test.runpytest("--bdd-json")
    assert (sample_test.tmpdir / "session_finish_results.json").exists()


def test_json_steps_keyword(sample_test):
    sample_test.runpytest("--bdd-json")

    with open(str(sample_test.tmpdir / "session_finish_results.json")) as f:
        data = json.load(f)

    steps = data[0]["steps"]
    assert steps[0]["type"] == "Given"
    assert steps[1]["type"] == "When"
    assert steps[2]["type"] == "And"
    assert steps[3]["type"] == "Then"


def test_json_steps_argument(sample_test):
    sample_test.runpytest("--bdd-json")

    with open(str(sample_test.tmpdir / "session_finish_results.json")) as f:
        data = json.load(f)

    steps = data[0]["steps"]
    assert steps[0]["step"] == "I have a scenario"
    assert steps[1]["step"] == "I start the test"
    assert steps[2]["step"] == "I know it will fails"
    assert steps[3]["step"] == "It fails"


def test_json_steps_status(sample_test):
    sample_test.runpytest("--bdd-json")

    with open(str(sample_test.tmpdir / "session_finish_results.json")) as f:
        data = json.load(f)

    steps = data[0]["steps"]
    assert steps[0]["status"] == "passed"
    assert steps[1]["status"] == "passed"
    assert steps[2]["status"] == "passed"
    assert steps[3]["status"] == "failed"


def test_json_steps_nodeid(sample_test):
    sample_test.runpytest("--bdd-json")

    with open(str(sample_test.tmpdir / "session_finish_results.json")) as f:
        data = json.load(f)

    steps = data[0]["steps"]
    assert steps[0]["nodeid"] != ""
    assert steps[1]["nodeid"] != ""
    assert steps[2]["nodeid"] != ""
    assert steps[3]["nodeid"] != ""


def test_json_steps_exception(sample_test):
    sample_test.runpytest("--bdd-json")

    with open(str(sample_test.tmpdir / "session_finish_results.json")) as f:
        data = json.load(f)

    steps = data[0]["steps"]
    assert steps[0]["exception"] == ""
    assert steps[1]["exception"] == ""
    assert steps[2]["exception"] == ""
    assert steps[3]["exception"] == "assert False"
