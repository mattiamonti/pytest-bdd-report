from abc import ABC, abstractmethod

from pytest_bdd_report.components.feature import Feature
from pytest_bdd_report.components.scenario import Scenario
from pytest_bdd_report.components.step import Step
from pytest_bdd_report.templates.feature_template import FeatureTemplate
from pytest_bdd_report.templates.scenario_template import ScenarioTemplate
from pytest_bdd_report.templates.step_template import StepTemplate
from pytest_bdd_report.templates.template import BaseTemplate


class BaseRenderer(ABC):
    @abstractmethod
    def render(self, items: list, template: BaseTemplate) -> str:
        ...


class StepRenderer(BaseRenderer):
    def render(self, items: list[Step], template: StepTemplate) -> str:
        rendered = ""
        for item in items:
            rendered += template.render_template(item)
        return rendered


class ScenarioRenderer(BaseRenderer):
    def render(self, items: list[Scenario], template: ScenarioTemplate) -> str:
        step_renderer = StepRenderer()
        step_template = StepTemplate()
        rendered = ""
        for item in items:
            rendered_steps = step_renderer.render(item.steps, step_template)
            rendered += template.render_template(item, rendered_steps)
        return rendered


class FeatureRenderer(BaseRenderer):
    def render(self, items: list[Feature], template: FeatureTemplate) -> str:
        scenario_renderer = ScenarioRenderer()
        scenario_template = ScenarioTemplate()
        rendered = ""
        for item in items:
            rendered_scenarios = scenario_renderer.render(
                item.scenarios, scenario_template
            )
            rendered += template.render_template(item, rendered_scenarios)
        return rendered
