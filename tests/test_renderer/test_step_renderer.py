from hypothesis import given, strategies as st
import pytest
from pytest_bdd_report.entities.step import Step
from pytest_bdd_report.entities.status_enum import Status
from pytest_bdd_report.templates.step_template import StepTemplate
from pytest_bdd_report.renderer.renderer import StepRenderer


@pytest.fixture
def mock_steps() -> list[Step]:
    return [
        Step("Given", "Step 1", 1, Status.PASSED, 16381916),
        Step("When", "Step 2", 1, Status.FAILED, 100039666),
        Step("Then", "Step 3", 1, Status.SKIPPED, 263386792),
    ]


@pytest.fixture
def mock_steps_with_seconds_duration() -> list[Step]:
    return [
        Step("Given", "Step 1", 1, Status.PASSED, 5005050375),
        Step("When", "Step 2", 1, Status.FAILED, 926849000),
    ]


@given(
    keyword=st.text(),
    name=st.text(),
    line=st.integers(),
    status=st.sampled_from(list(Status)),
    duration=st.integers(),
)
def test_step_rendering(
    keyword: str, name: str, line: int, status: Status, duration: int
):
    step = [Step(keyword, name, line, status, duration)]
    renderer = StepRenderer()

    rendered = renderer.render(step, StepTemplate())
    assert keyword in rendered
    assert name in rendered
    assert str(status.value) in rendered


def test_multiple_step_rendering(mock_steps: list[Step]):
    renderer = StepRenderer()

    rendered = renderer.render(mock_steps, StepTemplate())
    for step in mock_steps:
        assert step.keyword in rendered
        assert step.name in rendered
        assert str(step.status.value) in rendered


def test_step_duration_milliseconds(mock_steps: list[Step]):
    renderer = StepRenderer()

    rendered = renderer.render(mock_steps, StepTemplate())
    for step in mock_steps:
        assert f"{round((step.duration / 1_000_000), 3)}" in rendered


def test_step_duration_seconds(mock_steps_with_seconds_duration: list[Step]):
    renderer = StepRenderer()

    rendered = renderer.render(mock_steps_with_seconds_duration, StepTemplate())
    for step in mock_steps_with_seconds_duration:
        assert f"{round((step.duration / 1_000_000_000), 3)}" in rendered
