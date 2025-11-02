from pytest_bdd_report.entities.feature import Feature
from pytest_bdd_report.entities.scenario import Scenario
from pytest_bdd_report.entities.step import Step
from pytest_bdd_report.templates.scenario_template import ScenarioTemplate
from pytest_bdd_report.templates.step_template import StepTemplate
from pytest_bdd_report.templates.template import BaseTemplate
from pytest_bdd_report.renderer.renderer_protocol import Renderer


class StepRenderer:
    def render(self, items: list[Step], template: BaseTemplate) -> str:
        return "".join(template.render_template(item) for item in items)


class ScenarioRenderer:
    def __init__(self):
        self.step_renderer: Renderer = StepRenderer()
        self.step_template: StepTemplate = StepTemplate()

    def render(self, items: list[Scenario], template: BaseTemplate) -> str:
        rendered_steps = [
            self.step_renderer.render(item.steps, self.step_template) for item in items
        ]
        return "".join(
            template.render_template(item, steps)
            for item, steps in zip(items, rendered_steps)
        )


class FeatureRenderer:
    def __init__(self):
        self.scenario_renderer: Renderer = ScenarioRenderer()
        self.scenario_template: ScenarioTemplate = ScenarioTemplate()

    def render(self, items: list[Feature], template: BaseTemplate) -> str:
        rendered_scenarios = [
            self.scenario_renderer.render(item.scenarios, self.scenario_template)
            for item in items
        ]
        return "".join(
            template.render_template(item, scenarios)
            for item, scenarios in zip(items, rendered_scenarios)
        )


class FeatureStatisticsRenderer:
    def render(self, items: list[Feature], template: BaseTemplate) -> str:
        return "".join(template.render_template(item) for item in items)
