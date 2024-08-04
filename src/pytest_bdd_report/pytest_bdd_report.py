import pytest
from pytest_bdd_report.json_loader import JsonLoader
from pytest_bdd_report.report_composer import ReportComposer
from pytest_bdd_report.report import Report, ReportBuilder
from pytest_bdd_report.report_file_generator import ReportFileGenerator
from pytest_bdd_report.summary.summary_generator import SummaryGenerator
import os

BDD_REPORT_FLAG = "--bdd-report"
CUCUMBER_JSON_PATH = ".cucumber-data.json"


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
        config.option.cucumber_json_path = CUCUMBER_JSON_PATH


test_file_uri = []


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
            loader=JsonLoader(CUCUMBER_JSON_PATH),
            report_builder=ReportBuilder(report_name),
        )
        report = report_generator.create_report()
        summary = SummaryGenerator().populate_summary(report)
        file_generator = ReportFileGenerator()
        file_generator.create_report_file(
            report, summary, test_file_uri, report_file_path
        )
        print(test_file_uri)
