from abc import ABC, abstractmethod

from pytest_bdd_report.components.feature import Feature
from pytest_bdd_report.components.scenario import Scenario
from pytest_bdd_report.components.step import Step
from pytest_bdd_report.templates.feature_statistics_template import (
    FeatureStatisticsTemplate,
)
from pytest_bdd_report.templates.feature_template import FeatureTemplate
from pytest_bdd_report.templates.scenario_template import ScenarioTemplate
from pytest_bdd_report.templates.step_template import StepTemplate
from pytest_bdd_report.templates.template import BaseTemplate


class BaseRenderer(ABC):
    @abstractmethod
    def render(self, items: list, template: BaseTemplate) -> str:
        """
        Render the items into the template.
        @param items: to render
        @param template: in which render the items
        @return: rendered object
        """
        ...


class StepRenderer(BaseRenderer):
    def render(self, items: list[Step], template: BaseTemplate) -> str:
        return ''.join(template.render_template(item) for item in items)


class ScenarioRenderer(BaseRenderer):
    def __init__(self, step_renderer: StepRenderer = None):
        self.step_renderer = step_renderer or StepRenderer()

    def render(self, items: list[Scenario], template: BaseTemplate) -> str:
        rendered_steps = [self.step_renderer.render(item.steps, StepTemplate()) for item in items]
        return ''.join(template.render_template(item, steps) for item, steps in zip(items, rendered_steps))


class FeatureRenderer(BaseRenderer):
    def __init__(self, scenario_renderer: ScenarioRenderer = None):
        self.scenario_renderer = scenario_renderer or ScenarioRenderer()

    def render(self, items: list[Feature], template: BaseTemplate) -> str:
        rendered_scenarios = [self.scenario_renderer.render(item.scenarios, ScenarioTemplate()) for item in items]
        return ''.join(template.render_template(item, scenarios) for item, scenarios in zip(items, rendered_scenarios))



class FeatureStatisticsRenderer(BaseRenderer):
    def render(self, items: list[Feature], template: BaseTemplate) -> str:
        return ''.join(template.render_template(item) for item in items)
