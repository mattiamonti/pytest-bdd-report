import json
import pytest
import textwrap



def test_arguments_in_help(testdir):
    res = testdir.runpytest('--help')
    res.stdout.fnmatch_lines([
        '*bdd-json*',
        '*report*',
    ])

def test_json_message_in_stdout(testdir):
    res = testdir.runpytest('--bdd-json')
    res.stdout.fnmatch_lines([
        '*JSON with the tests result created successfully*',
    ])

def test_report_message_in_stdout(testdir):
    arg = "test"
    res = testdir.runpytest(f'--report={arg}')
    res.stdout.fnmatch_lines([
        f'*Report created at: {arg}*.html*',
    ])

def test_report_message_in_stdout_with_html(testdir):
    arg = "test.html"
    res = testdir.runpytest(f'--report={arg}')
    res.stdout.fnmatch_lines([
        f'*Report created at: {arg}*',
    ])

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


def test_create_json(sample_test_pass):
    sample_test_pass.runpytest('--bdd-json')
    assert (sample_test_pass.tmpdir / 'session_finish_results.json').exists()


def test_json_content_scenario_pass(sample_test_pass):
    sample_test_pass.runpytest('--bdd-json')

    with open(str(sample_test_pass.tmpdir / "session_finish_results.json")) as f:
        data = json.load(f)
    
    assert data[0]['nodeid'] != ""
    assert data[0]['feature'] == "Testing"
    assert data[0]['scenario'] == "Test scenario"
    assert data[0]['outcome'] == "passed"
    assert data[0]['duration'] != 0
    assert len(data[0]['steps']) == 2


def test_json_content_steps_pass(sample_test_pass):
    sample_test_pass.runpytest('--bdd-json')

    with open(str(sample_test_pass.tmpdir / "session_finish_results.json")) as f:
        data = json.load(f)
    
    assert len(data[0]['steps']) == 2
    assert data[0]['steps'][0]['nodeid'] != ""
    assert data[0]['steps'][0]['type'] == "Given"
    assert data[0]['steps'][0]['step'] == "I have a scenario"
    assert data[0]['steps'][0]['status'] == "passed"
    assert data[0]['steps'][1]['nodeid'] != ""
    assert data[0]['steps'][1]['type'] == "Then"
    assert data[0]['steps'][1]['step'] == "Should be created"
    assert data[0]['steps'][1]['status'] == "passed"


def test_json_content_scenario_fail(sample_test_fail):
    res = sample_test_fail.runpytest('--bdd-json')

    with open(str(sample_test_fail.tmpdir / "session_finish_results.json")) as f:
        data = json.load(f)
    
    res.assert_outcomes(failed=1)
    
    assert data[0]['nodeid'] != ""
    assert data[0]['feature'] == "Testing"
    assert data[0]['scenario'] == "Test scenario"
    assert data[0]['outcome'] == "failed"
    assert data[0]['duration'] != 0


def test_json_content_steps_fail(sample_test_fail):
    res = sample_test_fail.runpytest('--bdd-json')

    with open(str(sample_test_fail.tmpdir / "session_finish_results.json")) as f:
        data = json.load(f)
    
    res.assert_outcomes(failed=1)
    
    assert len(data[0]['steps']) == 2
    assert data[0]['steps'][0]['nodeid'] != ""
    assert data[0]['steps'][0]['type'] == "Given"
    assert data[0]['steps'][0]['step'] == "I have a scenario"
    assert data[0]['steps'][0]['status'] == "passed"
    assert data[0]['steps'][1]['nodeid'] != ""
    assert data[0]['steps'][1]['type'] == "Then"
    assert data[0]['steps'][1]['step'] == "Should be created"
    assert data[0]['steps'][1]['status'] == "failed"


