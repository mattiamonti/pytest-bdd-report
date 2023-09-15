from pytest_bdd_report.components.feature import Feature
from pytest_bdd_report.components.scenario import Scenario


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
    feature.add_scenario(Scenario(id="", name="", line=0, description="", tags=[], steps=[]))
    assert feature.scenarios == [Scenario(id="", name="", line=0, description="", tags=[], steps=[])]


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
    feature.add_scenario(Scenario(id="", name="", line=0, description="", tags=[], steps=[]))
    feature.add_scenario(Scenario(id="", name="", line=0, description="", tags=[], steps=[]))
    assert len(feature.scenarios) == 2
