from typing import override
from pytest_bdd_report.entities.feature import Feature
from pytest_bdd_report.entities.scenario import Scenario
from pytest_bdd_report.entities.step import Step
from pytest_bdd_report.templates.scenario_template import ScenarioTemplate
from pytest_bdd_report.templates.step_template import StepTemplate
from pytest_bdd_report.templates.template import BaseTemplate
from pytest_bdd_report.renderer.base_renderer import BaseRenderer


class StepRenderer(BaseRenderer[Step]):
    @override
    def render(self, items: list[Step], template: BaseTemplate) -> str:
        return "".join(template.render_template(item) for item in items)


class ScenarioRenderer(BaseRenderer[Scenario]):
    def __init__(self):
        self.step_renderer: BaseRenderer[Step] = StepRenderer()
        self.step_template: BaseTemplate = StepTemplate()

    @override
    def render(self, items: list[Scenario], template: BaseTemplate) -> str:
        rendered_steps = [
            self.step_renderer.render(item.steps, self.step_template) for item in items
        ]
        return "".join(
            template.render_template(item, steps)
            for item, steps in zip(items, rendered_steps)
        )


class FeatureRenderer(BaseRenderer[Feature]):
    def __init__(self):
        self.scenario_renderer: BaseRenderer[Scenario] = ScenarioRenderer()
        self.scenario_template: BaseTemplate = ScenarioTemplate()

    @override
    def render(self, items: list[Feature], template: BaseTemplate) -> str:
        rendered_scenarios = [
            self.scenario_renderer.render(item.scenarios, self.scenario_template)
            for item in items
        ]
        return "".join(
            template.render_template(item, scenarios)
            for item, scenarios in zip(items, rendered_scenarios)
        )


class FeatureStatisticsRenderer(BaseRenderer[list[Feature]]):
    @override
    def render(self, items: list[Feature], template: BaseTemplate) -> str:
        return "".join(template.render_template(item) for item in items)
