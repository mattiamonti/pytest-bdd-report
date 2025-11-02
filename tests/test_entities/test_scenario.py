from hypothesis import given
from hypothesis import strategies as st
from pytest_bdd_report.entities.scenario import Scenario
from pytest_bdd_report.entities.step import Step
from pytest_bdd_report.entities.status_enum import Status


@given(
    id=st.text(),
    name=st.text(),
    line=st.integers(),
    description=st.integers(),
    tags=st.dictionaries(st.sampled_from(["name"]), st.text()),
)
def test_init_scenario(
    id: str,
    name: str,
    line: int,
    description: str,
    tags: list[dict[str, str]],
):
    scenario = Scenario(
        id=id, name=name, line=line, description=description, tags=tags, steps=[]
    )

    assert scenario.id == id
    assert scenario.name == name
    assert scenario.line == line
    assert scenario.description == description
    assert scenario.tags == tags
    assert scenario.steps == []


@given(
    keyword=st.text(),
    name=st.text(),
    line=st.integers(),
    status=st.sampled_from(list(Status)),
    duration=st.integers(),
)
def test_add_step(keyword: str, name: str, line: int, status: Status, duration: int):
    scenario = Scenario(
        id="",
        name="",
        line=0,
        description="",
        tags=[],
        steps=[],
    )
    step = Step(keyword, name, line, status, duration)

    scenario.add_step(step)

    assert scenario.steps[0].keyword == keyword
    assert scenario.steps[0].name == name
    assert scenario.steps[0].line == line
    assert scenario.steps[0].status == status
    assert scenario.steps[0].duration == duration


def test_add_multiple_steps():
    scenario = Scenario(
        id="",
        name="",
        line=0,
        description="",
        tags=[],
        steps=[],
    )
    scenario.add_step(Step("Given", "name", 0, Status.PASSED, 0))
    scenario.add_step(Step("When", "name", 0, Status.PASSED, 0))
    assert len(scenario.steps) == 2
    assert scenario.steps[0].keyword == "Given"
    assert scenario.steps[1].keyword == "When"


@given(duration_1=st.integers(min_value=0), duration_2=st.integers(min_value=0))
def test_calculate_duration(duration_1: int, duration_2: int):
    scenario = Scenario(
        id="",
        name="",
        line=0,
        description="",
        tags=[],
        steps=[],
    )
    scenario.add_step(Step("Given", "name", 0, Status.PASSED, duration_1))
    scenario.add_step(Step("When", "name", 0, Status.PASSED, duration_2))
    expected_duration = (
        duration_1 + duration_2
    ) / 1_000_000_000  # from nanosecond to second
    scenario.calculate_duration()
    assert scenario.duration == expected_duration
