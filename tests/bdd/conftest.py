import shutil
import os
import pytest
from tests.bdd_generator.bdd_generator import (
    BDDFeature,
    BDDTestBuilder,
    BDDScenario,
    create_failed_step,
    create_passed_step,
    create_skipped_step,
)
from typing import Generator, Dict, List, Callable
from tests.bdd.fixtures.failed_scenario_modal_fixtures import *

@pytest.fixture()
def cleanup_bdd_generated():
    # Setup (se necessario)
    yield
    # Teardown
    folder = "generated_tests"
    if os.path.exists(folder) and os.path.isdir(folder):
        shutil.rmtree(folder)
    report = "generated_report.html"
    if os.path.exists(report) and os.path.isfile(report):
        os.remove(report)


ScenarioList = Dict[
    str, Dict[str, List[str]]
]  # feature -> {"passed": [...], "failed": [...]}


@pytest.fixture()
def generate_custom_bdd_report() -> Callable[[ScenarioList], str]:
    """
    Genera un report BDD personalizzato a partire da una struttura dict:
    {
        "Feature Name": {
            "passed": ["Scenario 1", "Scenario 2"],
            "failed": ["Scenario 3"]
        },
        ...
    }

    Returns:
        Callable[[dict], str]: funzione che genera il report e restituisce l'URL
    """

    def _generate(scenarios_by_feature: ScenarioList) -> str:
        test_dir = f"generated_tests"
        builder = BDDTestBuilder(test_dir)

        for feature_name, scenarios in scenarios_by_feature.items():
            feature = BDDFeature(feature_name)

            for scenario_name in scenarios.get("passed", []):
                scenario = BDDScenario(scenario_name)
                scenario.add_step(create_passed_step("Step 1 passed"))
                scenario.add_step(create_passed_step("Step 2 passed"))
                feature.add_scenario(scenario)

            for scenario_name in scenarios.get("failed", []):
                scenario = BDDScenario(scenario_name)
                scenario.add_step(create_passed_step("Step 1 passed"))
                scenario.add_step(create_passed_step("Step 2 passed"))
                scenario.add_step(create_failed_step("Step 3 failed"))
                feature.add_scenario(scenario)

            builder.add_feature(feature)

        builder.build()

        report_filename = f"generated_report.html"
        os.system(f"pytest --bdd-report={report_filename} {test_dir}/")

        return "file://" + os.path.abspath(report_filename)

    return _generate
