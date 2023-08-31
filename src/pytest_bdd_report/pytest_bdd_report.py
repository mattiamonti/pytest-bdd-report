# -*- coding: utf-8 -*-
# TODO scrivere test per questo plugin pytest
import os
import pytest
from pytest_bdd_report.utils.json_util import load_from_json, save_to_json
from pytest_bdd_report.collector.scenario_result_merger import ScenarioAndResultMerger
from pytest_bdd_report.collector.scenario_aggregator import ScenarioAggregator
from pytest_bdd_report.summary.summary import Summary

BDD_JSON_FLAG = "--bdd-json"
BDD_REPORT_FLAG = "--report"


# Command-line option setup
def pytest_addoption(parser):
    group = parser.getgroup("bdd-report")
    group.addoption(
        BDD_JSON_FLAG,
        action="store_true",
        default=False,
        help="Save the BDD tests result in json format.",
    )
    group.addoption(
        BDD_REPORT_FLAG,
        action="store",
        default="",
        help="Create the BDD tests report at the given path.",
    )


# Command-line option getter
def _get_cli_bool_flag_option(request, flag: str):
    return (
        request.config.getoption(flag) if hasattr(request.config, "getoption") else None
    )


def _get_cli_flag_option(request, flag: str):
    return request.config.getoption(flag)


def pytest_sessionstart(session):
    session.summary = Summary()
    session.results = dict()
    session.bdd_results = []  # session variable for steps information
    # remove, if exists, the old json containing the steps information
    if os.path.exists("bdd_results.json"):
        os.remove("bdd_results.json")
    # TODO aggiungere un titolo del report nel summary, magari scelto tramite linea di comando e fornirne uno di defaulkt (es. report-16/08/2023-15:40)


@pytest.hookimpl
def pytest_bdd_step_error(
    request, feature, scenario, step, step_func, step_func_args, exception
):
    """
    save the failed step information in a json file, appending it if the file is already created
    """
    # Ottieni le opzioni dalla linea di comando
    bdd_json_flag = _get_cli_bool_flag_option(request, BDD_JSON_FLAG)

    if bdd_json_flag:
        step_details = {
            "feature": feature.name,
            "scenario": scenario.name,
            "status": "failed",
            "type": step.keyword,
            "step": step.name,
            "exception": str(exception),
            "nodeid": step_func.__code__.co_filename + "::" + step_func.__name__,
        }
        # append the step details to the session variable
        request.session.bdd_results.append(step_details)


@pytest.hookimpl
def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    """
    save the step information in a json file, appending it if the file is already created
    """
    # Ottieni le opzioni dalla linea di comando
    bdd_json_flag = _get_cli_bool_flag_option(request, BDD_JSON_FLAG)

    if bdd_json_flag:
        step_details = {
            "feature": feature.name,
            "scenario": scenario.name,
            "status": "failed",
            "type": step.keyword,
            "step": step.name,
            "exception": "",
            "nodeid": step_func.__code__.co_filename + "::" + step_func.__name__,
        }
        # append the step details to the session variable
        request.session.bdd_results.append(step_details)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    test_result = outcome.get_result()
    if test_result.when == "call":
        # save the test results
        item.session.results[item] = test_result
        # update the tests summary
        if test_result.passed:
            item.session.summary.add_passed_test()
        elif test_result.failed:
            item.session.summary.add_failed_test()
        elif test_result.skipped:
            item.session.summary.add_skipped_test()
    if test_result.when == "setup" and test_result.skipped:
        item.session.summary.add_skipped_test()


# Helper function for the pytest_sessionfinish hook
def _load_aggregated_steps():
    """
    Load aggregated steps information from a JSON file.
    """
    return load_from_json("bdd_results.json")


def _load_tests_results(session):
    """
    Load test results from the pytest session.
    """
    session_results = list(session.results.values())
    return _get_tests_results(session_results)


def _merge_and_save_results(aggregated_steps, tests_results):
    """
    Merge aggregated steps information with test results and save to a JSON file.
    """
    aggregator = ScenarioAggregator()
    aggregated_steps_information = aggregator.aggregate_steps_into_scenario(
        aggregated_steps
    )

    merger = ScenarioAndResultMerger()
    final_results = merger.merge_scenario_and_result(
        aggregated_steps_information, tests_results
    )

    save_to_json(final_results, "session_finish_results.json")


def _get_tests_results(tests: list) -> list:
    """
    Get test results as a list of dictionaries.
    """
    results = []
    for test in tests:
        result_dict = {
            "nodeid": test.nodeid,
            "outcome": test.outcome,
            "keywords": test.keywords,
            "duration": test.duration,
            "sections": test.sections,
            "longrepr": test.longreprtext,
            "test_case": "",
            "when": test.when,
        }
        results.append(result_dict)
    return results


def pytest_sessionfinish(session):
    """
    Hook for pytest to perform tasks at the end of the session.
    """
    bdd_json_flag = _get_cli_bool_flag_option(session, BDD_JSON_FLAG)
    bdd_report_flag: str = _get_cli_flag_option(session, BDD_REPORT_FLAG)

    if bdd_json_flag:
        save_to_json(
            session.bdd_results, "bdd_results.json"
        )  # dump the session variable into the json
        aggregated_steps = _load_aggregated_steps()
        tests_results = _load_tests_results(session)
        _merge_and_save_results(aggregated_steps, tests_results)

        # create the summary of the features and save the summary to bdd_summary.json
        session.summary.create_feature_statistics("session_finish_results.json")
        session.summary.save_to_json("bdd_summary.json")

        # remove bdd_results.json
        if os.path.exists("bdd_results.json"):
            os.remove("bdd_results.json")

        print("\n\n📄 JSON with the tests result created successfully!")

    if bdd_report_flag:
        # TODO create report generation logic ecc... (maybe in another package)
        print(f"\n\n📈 Report created at: {bdd_report_flag.replace('.html', '')}.html")
