from hypothesis import given, strategies as st
import pytest
from pytest_bdd_report.entities.step import Step
from pytest_bdd_report.entities.scenario import Scenario
from pytest_bdd_report.entities.status_enum import Status
from pytest_bdd_report.templates.scenario_template import ScenarioTemplate
from pytest_bdd_report.renderer.renderer import ScenarioRenderer


@pytest.fixture
def mock_steps() -> list[Step]:
    return [
        Step("Given", "Step 1", 1, Status.PASSED, 16381916),
        Step("When", "Step 2", 1, Status.FAILED, 100039666),
        Step("Then", "Step 3", 1, Status.SKIPPED, 263386792),
    ]


@given(
    st.lists(
        st.builds(
            Scenario,
            id=st.text(min_size=1),
            name=st.text(min_size=1),
            line=st.integers(),
            description=st.text(),
            tags=st.lists(
                st.dictionaries(
                    st.sampled_from(["name"]), st.text(min_size=1), min_size=1
                ),
                min_size=1,
            ),
            steps=st.lists(
                st.builds(
                    Step,
                    keyword=st.text(min_size=1),
                    name=st.text(min_size=1),
                    line=st.integers(),
                    status=st.sampled_from(list(Status)),
                    duration=st.integers(),
                ),
                min_size=1,
            ),
        )
    ),
)
def test_scenario_rendering(scenarios: list[Scenario]):
    renderer = ScenarioRenderer()

    rendered = renderer.render(scenarios, ScenarioTemplate())
    for scenario in scenarios:
        assert scenario.name in rendered
        assert scenario.description in rendered
        for tag in scenario.tags:
            assert tag["name"] in rendered
        for step in scenario.steps:
            assert step.name in rendered


def test_scenario_without_tags(mock_steps: list[Step]):
    renderer = ScenarioRenderer()
    scenarios = [
        Scenario(
            id="abc",
            name="Sample scenario",
            line=0,
            description="abc",
            tags=[],
            steps=mock_steps,
        )
    ]

    rendered = renderer.render(scenarios, ScenarioTemplate())
    for scenario in scenarios:
        assert scenario.name in rendered
        assert scenario.description in rendered
        for step in scenario.steps:
            assert step.name in rendered
        assert "," not in rendered


def test_scenario_duration_seconds(mock_steps: list[Step]):
    renderer = ScenarioRenderer()
    scenario = Scenario(
        id="abc",
        name="Sample scenario",
        line=0,
        description="abc",
        tags=[],
        steps=mock_steps,
    )
    expected_duration = round(
        (sum(step.duration for step in scenario.steps) / 1_000_000_000), 3
    )

    rendered = renderer.render([scenario], ScenarioTemplate())
    assert str(expected_duration) in rendered


def test_scenario_duration_milliseconds(mock_steps: list[Step]):
    renderer = ScenarioRenderer()
    scenario = Scenario(
        id="abc",
        name="Sample scenario",
        line=0,
        description="abc",
        tags=[],
        steps=mock_steps[:1],
    )
    expected_duration = round(
        (sum(step.duration for step in scenario.steps) / 1_000_000), 3
    )

    rendered = renderer.render([scenario], ScenarioTemplate())
    assert str(expected_duration) in rendered
