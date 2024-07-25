import os

import pytest
import textwrap


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

@pytest.fixture()
def sample_test_with_utf_8_characters(testdir):
    testdir.makefile(
        ".feature",
        scenario=textwrap.dedent(
            """\
            Feature: Testing utf-8 characters like 👋 and 貓 feature
                Scenario: Testing utf-8 characters like 👋 and 貓 scenario
                    Given I include a 👋 character
                    Given I include a 貓 character
            """
        ),
    )

    testdir.makepyfile(
        textwrap.dedent(
            """\
        import pytest
        from pytest_bdd import given, when, then, scenario, parsers

        @scenario("scenario.feature", "Testing utf-8 characters like 👋 and 貓 scenario")
        def test_scenario():
            pass

        @given(parsers.parse("I include a {character} character"))
        def _(character):
            pass

        """
        )
    )
    return testdir


def test_arguments_in_help(testdir):
    res = testdir.runpytest("--help")
    res.stdout.fnmatch_lines(
        [
            "*bdd-report*",
        ]
    )


def test_create_html_report_file(sample_test):
    sample_test.runpytest("--bdd-report=report.html")
    assert (sample_test.tmpdir / "report.html").exists()


def test_create_html_report_file_with_directory(sample_test):
    sample_test.runpytest("--bdd-report=./reports/report.html")
    assert (sample_test.tmpdir / "./reports/report.html").exists()


def test_create_html_report_file_with_directory_name(sample_test):
    sample_test.runpytest("--bdd-report=results/report.html")
    assert (sample_test.tmpdir / "results/report.html").exists()


def test_create_html_report_file_with_directory_and_subdirectory(sample_test):
    sample_test.runpytest("--bdd-report=./reports/year/report.html")
    assert (sample_test.tmpdir / "./reports/year/report.html").exists()


def test_content_in_report(sample_test):
    sample_test.runpytest("--bdd-report=report.html")
    content = ""
    with open((sample_test.tmpdir / "report.html"), "r") as f:
        content = f.read()
    assert content != ""


def test_information_in_report(sample_test):
    sample_test.runpytest("--bdd-report=report.html")
    content = ""
    with open((sample_test.tmpdir / "report.html"), "r") as f:
        content = f.read()
    assert "Testing" in content
    assert "Test scenario" in content
    assert "I have a scenario" in content
    assert "I start the test" in content
    assert "I know it will fails" in content
    assert " It fails" in content

def test_utf_8_information_in_report(sample_test_with_utf_8_characters):
    sample_test_with_utf_8_characters.runpytest("--bdd-report=report.html")
    content = ""
    with open((sample_test_with_utf_8_characters.tmpdir / "report.html"), "r", encoding="utf-8") as f:
        content = f.read()
    assert "Testing utf-8 characters like 👋 and 貓 feature" in content
    assert "Testing utf-8 characters like 👋 and 貓 scenario" in content
    assert 'I include a 👋 character' in content
    assert 'I include a 貓 character' in content
