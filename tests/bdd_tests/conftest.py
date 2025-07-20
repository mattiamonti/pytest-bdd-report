import shutil
import os
import pytest
from tests.bdd_generator.bdd_generator import BDDFeature, BDDTestBuilder, BDDScenario, create_failed_step, create_passed_step, create_skipped_step


@pytest.fixture()
def cleanup_bdd_generated():
    # Setup (se necessario)
    yield
    # Teardown
    folder = "generated_tests"
    if os.path.exists(folder) and os.path.isdir(folder):
        shutil.rmtree(folder)
    report = "proto_bdd_testing.html"
    if os.path.exists(report) and os.path.isfile(report):
        os.remove(report)
    
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