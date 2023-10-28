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
    def render(self, items: list[Step], template: StepTemplate) -> str:
        rendered = ""
        for item in items:
            rendered += template.render_template(item)
        return rendered


class ScenarioRenderer(BaseRenderer):
    def __init__(self, step_renderer: StepRenderer = None):
        self.step_renderer = step_renderer or StepRenderer()

    def render(self, items: list[Scenario], template: ScenarioTemplate) -> str:
        rendered = ""
        for item in items:
            rendered_steps = self.step_renderer.render(item.steps, StepTemplate())
            rendered += template.render_template(item, rendered_steps)
        return rendered


class FeatureRenderer(BaseRenderer):
    def __init__(self, scenario_renderer: ScenarioRenderer = None):
        self.scenario_renderer = scenario_renderer or ScenarioRenderer()

    def render(self, items: list[Feature], template: FeatureTemplate) -> str:
        rendered = ""
        for item in items:
            rendered_scenarios = self.scenario_renderer.render(
                item.scenarios, ScenarioTemplate()
            )
            rendered += template.render_template(item, rendered_scenarios)
        return rendered


class FeatureStatisticsRenderer(BaseRenderer):
    def render(self, items: list[Feature], template: FeatureStatisticsTemplate) -> str:
        rendered = ""
        for item in items:
            rendered += template.render_template(item)
        return rendered
