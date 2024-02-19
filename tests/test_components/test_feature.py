from src.pytest_bdd_report.components.feature import Feature
from src.pytest_bdd_report.components.scenario import Scenario
import pytest

def test_add_scenario():
    feature = Feature(
        id="",
        name="",
        line=0,
        description="",
        tags=[],
        uri="",
        scenarios=[],
    )
    feature.add_scenario(
        Scenario(id="", name="", line=0, description="", tags=[], steps=[])
    )
    assert feature.scenarios == [
        Scenario(id="", name="", line=0, description="", tags=[], steps=[])
    ]


def test_add_multiple_scenarios():
    feature = Feature(
        id="",
        name="",
        line=0,
        description="",
        tags=[],
        uri="",
        scenarios=[],
    )
    feature.add_scenario(
        Scenario(id="", name="", line=0, description="", tags=[], steps=[])
    )
    feature.add_scenario(
        Scenario(id="", name="", line=0, description="", tags=[], steps=[])
    )
    assert len(feature.scenarios) == 2


def test_calculate_duration():
    feature = Feature(
        id="",
        name="",
        line=0,
        description="",
        tags=[],
        uri="",
        scenarios=[],
    )
    feature.add_scenario(
        Scenario(id="", name="", line=0, description="", tags=[], steps=[], duration=1)
    )
    feature.add_scenario(
        Scenario(
            id="", name="", line=0, description="", tags=[], steps=[], duration=2.5
        )
    )
    feature.calculate_duration()
    assert feature.duration == 3.5


def test_calculate_duration_no_scenarios():
    # Test calculating duration with no scenarios
    feature = Feature(id="", name="", line=0, description="", tags=[], uri="", scenarios=[])
    feature.calculate_duration()
    assert feature.duration == 0

