import os
from pathlib import Path
from textwrap import dedent
from typing import List, Optional


class BDDFeature:
    def __init__(self, name: Optional[str] = None):
        self.name = name or "Auto Feature"
        self.scenarios: List[BDDScenario] = []

    def add_scenario(self, scenario: 'BDDScenario'):
        self.scenarios.append(scenario)


class BDDScenario:
    def __init__(self, name: Optional[str] = None):
        self.name = name or "Auto Scenario"
        self.steps: List[BDDStep] = []

    def add_step(self, step: 'BDDStep'):
        self.steps.append(step)


class BDDStep:
    def __init__(self, name: Optional[str] = None, outcome: str = "pass"):
        self.name = name or "auto step"
        self.outcome = outcome  # one of: pass, fail, skip


class BDDTestBuilder:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.features: List[BDDFeature] = []
        self.step_defs: List[str] = []
        self.test_funcs: List[str] = []

    def add_feature(self, feature: BDDFeature):
        self.features.append(feature)

    def build(self):
        all_step_names = set()
        for i, feature in enumerate(self.features, 1):
            feature_filename = f"feature_{i}.feature"
            feature_path = self.output_dir / feature_filename
            with open(feature_path, "w") as f:
                f.write(f"Feature: {feature.name}\n")
                for j, scenario in enumerate(feature.scenarios, 1):
                    scenario_name = scenario.name
                    f.write(f"  Scenario: {scenario_name}\n")
                    for step in scenario.steps:
                        line = f"    Given {step.name}\n"
                        f.write(line)
                        step_func_name = self._sanitize_name(step.name)
                        if step_func_name not in all_step_names:
                            self.step_defs.append(self._generate_step_function(step_func_name, step.name, step.outcome))
                            all_step_names.add(step_func_name)

                    self.test_funcs.append(self._generate_test_function(feature_filename, scenario_name))

        self._write_steps()

    def _sanitize_name(self, name: str) -> str:
        return name.lower().replace(" ", "_").replace("-", "_")

    def _generate_step_function(self, func_name: str, step_text: str, outcome: str) -> str:
        outcome_map = {
            "pass": "    pass",
            "fail": '    raise AssertionError("Step failed intentionally")',
            "skip": '    pytest.skip("Step skipped intentionally")'
        }
        body = outcome_map.get(outcome)
        return dedent(f"""
        @given("{step_text}")
        def {func_name}(request):
            {body}
        """).strip()

    def _generate_test_function(self, feature_file: str, scenario_name: str) -> str:
        test_name = "test_" + self._sanitize_name(scenario_name)
        return dedent(f"""
        @scenario("{feature_file}", "{scenario_name}")
        def {test_name}():
            pass
        """).strip()

    def _write_steps(self):
        steps_path = self.output_dir / "test_steps.py"
        with open(steps_path, "w") as f:
            f.write("import pytest\n")
            f.write("from pytest_bdd import given, scenario\n\n")
            f.write("\n\n".join(self.step_defs))
            f.write("\n\n\n")
            f.write("\n\n".join(self.test_funcs))


def create_passed_step(name: Optional[str] = None) -> BDDStep:
    return BDDStep(name=name, outcome="pass")


def create_failed_step(name: Optional[str] = None) -> BDDStep:
    return BDDStep(name=name, outcome="fail")


def create_skipped_step(name: Optional[str] = None) -> BDDStep:
    return BDDStep(name=name, outcome="skip")

def create_scenario_fantastico(name: str = None):
    pass

if __name__ == "__main__":
    builder = BDDTestBuilder("generated_tests_iter_2")

    feature = BDDFeature("Feature autogenerata")

    scenario1 = BDDScenario("Scenario passato")
    scenario1.add_step(create_passed_step("lo step è passato"))
    scenario1.add_step(create_passed_step("lo step è passato"))
    scenario1.add_step(create_passed_step("lo step è passato"))

    scenario2 = BDDScenario("Scenario fallito")
    scenario2.add_step(create_passed_step("lo step è passato"))
    scenario2.add_step(create_passed_step("lo step è passato"))
    scenario2.add_step(create_failed_step("lo step fallisce"))

    scenario3 = BDDScenario("Scenario skippato")
    scenario3.add_step(create_skipped_step("lo step viene skippato"))
    scenario3.add_step(create_passed_step("lo step è passato"))
    scenario3.add_step(create_passed_step("lo step è passato"))

    feature.add_scenario(scenario1)
    feature.add_scenario(scenario2)
    feature.add_scenario(scenario3)

    builder.add_feature(feature)
    builder.build()