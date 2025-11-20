import pytest
from pytest_bdd_report.loader.json_loader import JsonLoader
from pytest_bdd_report.report.report_composer import ReportComposer
from pytest_bdd_report.report.report import ReportBuilder
from pytest_bdd_report.report.report_file import ReportFileBuilder
from pytest_bdd_report.summary.summary_generator import SummaryGenerator
import os

BDD_REPORT_FLAG = "--bdd-report"
DEFAULT_CUCUMBER_JSON_PATH = ".cucumber-data.json"
test_file_uri: list[str] = []


# Command-line option setup
def pytest_addoption(parser):
    """
    Add the command line option to generate the HTML report
    """
    group = parser.getgroup("bdd-report")
    group.addoption(
        BDD_REPORT_FLAG,
        action="store",
        default="",
        help="Create the BDD tests report at the given path.",
    )


# Command-line option getter
def _get_flag_option(config, flag: str) -> str:
    """
    @return the option value
    """
    return config.getoption(flag).replace(".html", "") + ".html"


def pytest_configure(config):
    """
    Configure the generation of the cucumber-json file
    """
    if _get_flag_option(config, BDD_REPORT_FLAG) != ".html":
        cucumber_path = config.option.cucumber_json_path
        if not cucumber_path or cucumber_path == "":
            cucumber_path = DEFAULT_CUCUMBER_JSON_PATH
            config.option.cucumber_json_path = cucumber_path

        parent_directories = os.path.dirname(cucumber_path)
        if parent_directories and not os.path.exists(parent_directories):
            os.makedirs(parent_directories)


def pytest_collection_modifyitems(config, items):
    if _get_flag_option(config, BDD_REPORT_FLAG) != ".html":
        for item in items:
            uri = item.nodeid.split("::")[0]
            if uri not in test_file_uri:
                test_file_uri.append(uri)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Log the report file path in the teminal
    """
    bdd_report_flag = _get_flag_option(config, BDD_REPORT_FLAG)
    if bdd_report_flag != ".html":
        print(f"\n\n Report created at: {bdd_report_flag}")


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session):
    """
    Run the plugin logic after the entire test session execution
    """
    report_file_path = _get_flag_option(session.config, BDD_REPORT_FLAG)
    if report_file_path != ".html":
        report_name = os.path.basename(report_file_path)
        report_generator = ReportComposer(
            loader=JsonLoader(session.config.option.cucumber_json_path),
            report_builder=ReportBuilder(report_name),
        )
        report = report_generator.create_report()
        summary = SummaryGenerator().populate_summary(report)

        report_file = (
            ReportFileBuilder()
            .add_report(report)
            .add_summary(summary)
            .add_test_file_uri(test_file_uri)
            .build()
        )

        report_file.create(report_file_path)
