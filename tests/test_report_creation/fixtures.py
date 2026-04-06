import textwrap

import pytest


@pytest.fixture()
def sample_test(testdir: pytest.Testdir) -> pytest.Testdir:
    _ = testdir.makefile(
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

    _ = testdir.makepyfile(
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
def sample_test_with_utf_8_characters(testdir: pytest.Testdir) -> pytest.Testdir:
    _ = testdir.makefile(
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

    _ = testdir.makepyfile(
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


@pytest.fixture()
def empty_test(testdir: pytest.Testdir) -> pytest.Testdir:
    _ = testdir.makefile(
        ".feature",
        scenario=textwrap.dedent(
            """\
            """
        ),
    )

    _ = testdir.makepyfile(
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
def fixture_error_test(testdir: pytest.Testdir) -> pytest.Testdir:
    _ = testdir.makefile(
        ".feature",
        scenario=textwrap.dedent(
            """\
            """
        ),
    )

    _ = testdir.makepyfile(
        textwrap.dedent(
            """\
            import pytest


            @pytest.fixture(autouse=True)
            def broken_fixture():
                raise Exception(f"Exception here!")

            def test_smth():
                assert True
        """
        )
    )

    return testdir


@pytest.fixture()
def no_bdd_test(testdir: pytest.Testdir) -> pytest.Testdir:
    _ = testdir.makefile(
        ".feature",
        scenario=textwrap.dedent(
            """\
            """
        ),
    )

    _ = testdir.makepyfile(
        textwrap.dedent(
            """\
            import pytest

            def unit_test_foo():
                assert True

            def unit_test_bar():
                assert False
        """
        )
    )

    return testdir


@pytest.fixture()
def sample_test_with_step_attachments(testdir: pytest.Testdir) -> pytest.Testdir:
    _ = testdir.makefile(
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

    _ = testdir.makepyfile(
        textwrap.dedent(
            """\
        import pytest
        from pytest_bdd import given, when, then, scenario
        from pytest_bdd_report import attach

        @scenario("scenario.feature", "Test scenario")
        def test_scenario():
            pass

        @given("I have a scenario")
        def _():
            attach.text_to_step("Test text attachment", "Given", "I have a scenario")
            pass

        @when("I start the test")
        def _():
            attach.json_to_step({"test":"json attachment"}, "When", "I start the test")
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
