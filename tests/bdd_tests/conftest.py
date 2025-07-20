import shutil
import os
import pytest
from tests.bdd_generator.bdd_generator import BDDFeature, BDDTestBuilder, BDDScenario, create_failed_step, create_passed_step, create_skipped_step
from typing import Generator, Dict, List, Callable


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
    
@pytest.fixture()
def generate_report_with_failed_scenarios() -> Generator[[int], str, None]:
    """
    Pytest fixture parametrizzabile per generare un report con N scenari falliti.

    Usage:
        def test_something(generate_report_with_failed_scenarios):
            report_url = generate_report_with_failed_scenarios(3)
    """
    def _generate(scenario_count: int) -> str:
        builder = BDDTestBuilder("generated_tests")
        feature = BDDFeature("Testing failed scenarios links")

        for i in range(1, scenario_count + 1):
            scenario = BDDScenario(f"Failed {i}")
            scenario.add_step(create_passed_step("a passed step"))
            scenario.add_step(create_passed_step("a passed step"))
            scenario.add_step(create_failed_step("a failed step"))
            feature.add_scenario(scenario)

        builder.add_feature(feature)
        builder.build()

        os.system("pytest --bdd-report=proto_bdd_testing.html generated_tests/")

        path = os.path.abspath("proto_bdd_testing.html")
        return "file://" + path

    return _generate

@pytest.fixture()
def generate_report_with_one_failed_feature() -> str:
    """
    Generate the test files and report with one feature with one failed scenario

    Returns:
        str: the report URI
    """
    builder = BDDTestBuilder("generated_tests")
    feature = BDDFeature("Testing failed scenarios links")
    scenario1 = BDDScenario("Failed 1")
    scenario1.add_step(create_passed_step("lo step è passato"))
    scenario1.add_step(create_passed_step("lo step è passato"))
    scenario1.add_step(create_failed_step("lo step è fallito"))
    feature.add_scenario(scenario1)
    builder.add_feature(feature)
    builder.build()

    os.system("pytest --bdd-report=proto_bdd_testing.html generated_tests/")

    path = os.path.abspath("proto_bdd_testing.html")
    file_url = "file://" + path
    return file_url

@pytest.fixture()
def generate_report_with_feature_with_multiple_failed_scenarios() -> str:
    """
    Generate the test files and report with one feature with multiple failed scenarios

    Returns:
        str: the report URI
    """
    builder = BDDTestBuilder("generated_tests")
    feature = BDDFeature("Testing failed scenarios links")
    scenario1 = BDDScenario("Failed 1")
    scenario1.add_step(create_passed_step("a passed step"))
    scenario1.add_step(create_passed_step("a passed step"))
    scenario1.add_step(create_failed_step("a failed step"))
    feature.add_scenario(scenario1)
    scenario2 = BDDScenario("Failed 2")
    scenario2.add_step(create_passed_step("a passed step"))
    scenario2.add_step(create_passed_step("a passed step"))
    scenario2.add_step(create_failed_step("a failed step"))
    feature.add_scenario(scenario2)
    scenario3 = BDDScenario("Failed 3")
    scenario3.add_step(create_passed_step("a passed step"))
    scenario3.add_step(create_passed_step("a passed step"))
    scenario3.add_step(create_failed_step("a failed step"))
    feature.add_scenario(scenario3)
    builder.add_feature(feature)
    builder.build()

    os.system("pytest --bdd-report=proto_bdd_testing.html generated_tests/")

    path = os.path.abspath("proto_bdd_testing.html")
    file_url = "file://" + path
    return file_url


ScenarioList = Dict[str, Dict[str, List[str]]]  # feature -> {"passed": [...], "failed": [...]}

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