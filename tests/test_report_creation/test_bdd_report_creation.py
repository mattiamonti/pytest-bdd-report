import pytest

from tests.test_report_creation.fixtures import (
    empty_test,
    fixture_error_test,
    no_bdd_test,
    sample_test,
    sample_test_with_utf_8_characters,
)


def test_arguments_in_help(testdir: pytest.Testdir):
    res = testdir.runpytest("--help")
    res.stdout.fnmatch_lines(
        [
            "*bdd-report*",
        ]
    )


def test_create_report_without_bdd_tests(empty_test: pytest.Testdir):
    """Reproduce the issue #41"""
    res = empty_test.runpytest("--bdd-report=empty")
    assert "ZeroDivisionError" not in res.stderr.str()
    assert (empty_test.tmpdir / "empty.html").exists()


def test_create_report_with_fixture_error(fixture_error_test: pytest.Testdir):
    """Reproduce the issue #41"""
    res = fixture_error_test.runpytest("--bdd-report=empty")
    assert "ZeroDivisionError" not in res.stderr.str()
    assert (fixture_error_test.tmpdir / "empty.html").exists()


def test_create_report_with_no_bdd_tests(no_bdd_test: pytest.Testdir):
    """Reproduce the issue #41"""
    res = no_bdd_test.runpytest("--bdd-report=empty")
    assert "ZeroDivisionError" not in res.stderr.str()
    assert (no_bdd_test.tmpdir / "empty.html").exists()


@pytest.mark.parametrize(
    "directory, name",
    [
        ("", "report.html"),
        ("", "report"),
        ("./", "report.html"),
        ("./", "report"),
        ("./reports/", "report_name.html"),
        ("./reports/", "report_name"),
        ("reports/", "report_name.html"),
        ("reports/", "report_name"),
        ("./reports/year/", "report_name.html"),
        ("./reports/year/", "report_name"),
        ("reports/year/", "report_name.html"),
        ("reports/year/", "report_name"),
    ],
)
def test_create_report_with_custom_name_and_directory(
    sample_test: pytest.Testdir, name: str, directory: str
):
    report_path = name
    if directory != "":
        report_path = f"{directory}/{name}"

    sample_test.runpytest(f"--bdd-report={report_path}")

    report_path = report_path.replace(".html", "") + ".html"
    assert (sample_test.tmpdir / report_path).exists()


@pytest.mark.parametrize(
    "directory, name",
    [
        ("", "custom_cucumber.json"),
        ("./", "custom_cucumber.json"),
        ("./reports/", "custom_cucumber.json"),
        ("reports/", "custom_cucumber.json"),
        ("./reports/year/", "custom_cucumber.json"),
        ("reports/year/", "custom_cucumber.json"),
    ],
)
def test_create_report_with_custom_cucumber_json_path(
    sample_test: pytest.Testdir, name: str, directory: str
):
    cucumber_path = name
    if directory != "":
        cucumber_path = f"{directory}/{name}"

    sample_test.runpytest(
        "--bdd-report=report.html", f"--cucumber-json={cucumber_path}"
    )

    assert (sample_test.tmpdir / cucumber_path).exists()
    assert (sample_test.tmpdir / "report.html").exists()


def test_create_html_report_with_custom_cucumber_path_without_existing_directory(
    sample_test: pytest.Testdir,
):
    sample_test.runpytest(
        "--bdd-report=custom_cucumber_report.html",
        "--cucumber-json=cucumber_dir/custom_cucumber_file.json",
    )
    assert (sample_test.tmpdir / "custom_cucumber_report.html").exists()
    assert (sample_test.tmpdir / "cucumber_dir" / "custom_cucumber_file.json").exists()


def test_create_html_report_with_custom_cucumber_path_both_without_existing_directory(
    sample_test: pytest.Testdir,
):
    sample_test.runpytest(
        "--bdd-report=report_dir/custom_cucumber_report.html",
        "--cucumber-json=cucumber_dir/custom_cucumber_file.json",
    )
    assert (sample_test.tmpdir / "report_dir" / "custom_cucumber_report.html").exists()
    assert (sample_test.tmpdir / "cucumber_dir" / "custom_cucumber_file.json").exists()


def test_utf_8_information_in_report(sample_test_with_utf_8_characters: pytest.Testdir):
    sample_test_with_utf_8_characters.runpytest("--bdd-report=report.html")
    content = ""
    with open(
        (sample_test_with_utf_8_characters.tmpdir / "report.html"),
        "r",
        encoding="utf-8",
    ) as f:
        content = f.read()
    assert "Testing utf-8 characters like 👋 and 貓 feature" in content
    assert "Testing utf-8 characters like 👋 and 貓 scenario" in content
    assert "I include a 👋 character" in content
    assert "I include a 貓 character" in content
