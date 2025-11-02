from pytest_bdd_report.entities.feature import Feature
from pytest_bdd_report.entities.scenario import Scenario
import pytest
from hypothesis import given
from hypothesis import strategies as st


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
    feature = Feature(
        id="", name="", line=0, description="", tags=[], uri="", scenarios=[]
    )
    feature.calculate_duration()
    assert feature.duration == 0


@given(
    id=st.text(min_size=1),
    name=st.text(min_size=1),
    line=st.integers(min_value=0),
    description=st.text(),
    uri=st.text(min_size=1),
    scenarios=st.lists(
        st.builds(
            Scenario,
            id=st.text(min_size=1),
            name=st.text(min_size=1),
            line=st.integers(min_value=0),
            description=st.text(),
            duration=st.floats(min_value=0.1),
        )
    ),
)
def test_create_feature(
    id: str,
    name: str,
    line: int,
    description: str,
    uri: str,
    scenarios: list[Scenario],
):
    feature = Feature(
        id=id,
        name=name,
        line=line,
        description=description,
        tags=[],
        uri=uri,
        scenarios=scenarios,
    )

    assert feature.id == id
    assert feature.name == name
    assert feature.line == line
    assert feature.description == description
    assert feature.tags == []
    assert feature.uri == uri
    assert feature.scenarios == scenarios
