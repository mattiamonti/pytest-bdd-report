# -*- coding: utf-8 -*-
# TODO scrivere test per questo plugin pytest
import os
import pytest
from utils.json_util import load_from_json, save_to_json
from collector.scenario_result_merger import ScenarioAndResultMerger
from collector.scenario_aggregator import ScenarioAggregator
from collector.step_details import StepDetails
from summary.summary import Summary


def pytest_addoption(parser):
    group = parser.getgroup("bdd-report")
    group.addoption(
        "--saveit", action="store_true", default=False, help="print something."
    )


# initializa the summary of the tests
# summary = None


def pytest_sessionstart(session):
    session.summary = Summary()
    session.results = dict()
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
    saveit_option = (
        request.config.getoption("--saveit")
        if hasattr(request.config, "getoption")
        else None
    )

    if saveit_option:
        step_details = StepDetails(
            feature=feature.name,
            scenario=scenario.name,
            status="failed",
            type=step.keyword,
            step=step.name,
            exception=str(exception),
            nodeid=step_func.__code__.co_filename + "::" + step_func.__name__,
        )
        step_details.append_to_json("bdd_results.json")


@pytest.hookimpl
def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    """
    save the step information in a json file, appending it if the file is already created
    """
    # Ottieni le opzioni dalla linea di comando
    saveit_option = (
        request.config.getoption("--saveit")
        if hasattr(request.config, "getoption")
        else None
    )

    if saveit_option:
        step_details = StepDetails(
            feature=feature.name,
            scenario=scenario.name,
            status="passed",
            type=step.keyword,
            step=step.name,
            exception="",
            nodeid=f"{step_func.__code__.co_filename}::{step_func.__name__}",
        )
        step_details.append_to_json("bdd_results.json")


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


def pytest_sessionfinish(session):
    """
    Hook for pytest to perform tasks at the end of the session.
    """
    saveit_option = (
        session.config.getoption("--saveit")
        if hasattr(session.config, "getoption")
        else None
    )

    if saveit_option:
        aggregated_steps = _load_aggregated_steps()
        tests_results = _load_tests_results(session)
        _merge_and_save_results(aggregated_steps, tests_results)

        # save the summary of the tests
        session.summary.save_to_json("bdd_summary.json")


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
