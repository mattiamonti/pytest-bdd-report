from playwright.sync_api import Page, Locator, expect
import pytest
from tests.bdd.elements.scenario_pom import ScenarioPOM
from tests.bdd.utils.duration import get_duration


class StepPOM:
    def __init__(self, step: Locator) -> None:
        self.step = step

    def get_duration(self) -> float:
        return get_duration(self.step)

    def get_text(self) -> str:
        return self.step.inner_text().strip()
