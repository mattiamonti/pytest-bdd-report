from hypothesis import given
from hypothesis import strategies as st
from pytest_bdd_report.entities.status_enum import Status
from pytest_bdd_report.entities.step import Step


@given(
    keyword=st.text(),
    name=st.text(),
    line=st.integers(),
    status=st.sampled_from(list(Status)),
    duration=st.integers(),
)
def test_init_step(keyword: str, name: str, line: int, status: Status, duration: int):
    step = Step(keyword, name, line, status, duration)

    assert step.keyword == keyword
    assert step.name == name
    assert step.line == line
    assert step.status == status
    assert step.duration == duration
    assert step.error_message == ""


@given(error_message=st.text(min_size=1))
def test_step_with_error_message(error_message: str) -> None:
    keyword = "Given"
    name = "Sample step name"
    line = 10
    status = Status.FAILED
    duration = 10250

    step = Step(keyword, name, line, status, duration, error_message)

    assert step.keyword == keyword
    assert step.name == name
    assert step.line == line
    assert step.status == status
    assert step.duration == duration
    assert step.error_message == error_message
