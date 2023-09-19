import os
import pytest
from pytest_bdd_report.json_loader import JsonLoader
from pytest_bdd_report.report_generator import ReportGenerator, Report
from pytest_bdd_report.report_file_generator import ReportFileGenerator

BDD_REPORT_FLAG = "--bdd-report"


# Command-line option setup
def pytest_addoption(parser):
    group = parser.getgroup("bdd-report")
    group.addoption(
        BDD_REPORT_FLAG,
        action="store",
        default="",
        help="Create the BDD tests report at the given path.",
    )


# Command-line option getter
def _get_cli_flag_option(request, flag: str) -> str:
    return request.config.getoption(flag)


def pytest_configure(config):
    # Configurare per usare il json creato direttamente da pytest-bdd
    if config.getoption(BDD_REPORT_FLAG):
        config.option.cucumber_json_path = (
            "prova_report_cucumber_automatico.json"  # duration in nanosecond
        )


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session):
    """
    Hook for pytest to perform tasks at the end of the session.
    """
    bdd_report_flag = _get_cli_flag_option(session, BDD_REPORT_FLAG)

    if bdd_report_flag:
        # TODO implement report generation logic ecc... (maybe in another package)
        report_name = bdd_report_flag.replace(".html", "")
        print(f"\n\n📈 Report created at: {report_name}.html")

        json_data = JsonLoader.load_json("prova_report_cucumber_automatico.json")
        report = Report("prova", [])
        report_generator = ReportGenerator(json_data, report)
        report = report_generator.create_report()
        renderer = ReportFileGenerator()
        renderer.create_report_file(report, f"{report_name}.html")
