import json

import pytest
from hypothesis import given
from hypothesis import strategies as st

from pytest_bdd_report import attach
from pytest_bdd_report.extensions.step_information import step_information_repo


@given(
    step_keyword=st.permutations(["Given", "When", "And", "Then"]),
    step_name=st.text(min_size=1),
    text_information=st.text(min_size=1),
)
def test_attach_text_to_step(step_keyword: str, step_name: str, text_information: str):
    attach.text_to_step(text_information, step_keyword, step_name)

    assert len(step_information_repo.repo) == 1
    step_info = step_information_repo.get(step_keyword, step_name)
    assert step_info is not None
    step_information_repo.repo.remove(step_info)  # Clean the repository after the test
    assert step_info.step_keyword == step_keyword
    assert step_info.step_name == step_name
    assert step_info.text != []
    assert step_info.text[0] == text_information
    assert step_info.json == []


@given(
    step_keyword=st.permutations(["Given", "When", "And", "Then"]),
    step_name=st.text(min_size=1),
    text_informations=st.lists(elements=st.text(min_size=1), min_size=1),
)
def test_attach_more_text_to_step(
    step_keyword: str, step_name: str, text_informations: list[str]
):
    for text_info in text_informations:
        attach.text_to_step(text_info, step_keyword, step_name)

    assert len(step_information_repo.repo) == 1
    step_info = step_information_repo.get(step_keyword, step_name)
    assert step_info is not None
    step_information_repo.repo.remove(step_info)  # Clean the repository after the test
    assert step_info.step_keyword == step_keyword
    assert step_info.step_name == step_name
    assert step_info.text != []
    assert len(step_info.text) == len(text_informations)
    for text_info in text_informations:
        assert text_info in step_info.text


@given(
    step_keyword=st.permutations(["Given", "When", "And", "Then"]),
    step_name=st.text(min_size=1),
    json_information=st.dictionaries(
        keys=st.text(min_size=1),
        values=st.text(min_size=1),
        min_size=1,
    ),
)
def test_attach_json_to_step(step_keyword: str, step_name: str, json_information: dict):
    attach.json_to_step(json_information, step_keyword, step_name)

    formatted_json_information = json.dumps(json_information, indent=2).strip()

    assert len(step_information_repo.repo) == 1
    step_info = step_information_repo.get(step_keyword, step_name)
    assert step_info is not None
    step_information_repo.repo.remove(step_info)  # Clean the repository after the test
    assert step_info.step_keyword == step_keyword
    assert step_info.step_name == step_name
    assert step_info.json != []
    assert step_info.json[0] == formatted_json_information
    assert step_info.text == []


@given(
    step_keyword=st.permutations(["Given", "When", "And", "Then"]),
    step_name=st.text(min_size=1),
    json_informations=st.lists(
        elements=st.dictionaries(
            keys=st.text(min_size=1),
            values=st.text(min_size=1),
            min_size=1,
        ),
        min_size=1,
    ),
)
def test_attach_more_json_to_step(
    step_keyword: str, step_name: str, json_informations: list[dict]
):
    for json_info in json_informations:
        attach.json_to_step(json_info, step_keyword, step_name)

    assert len(step_information_repo.repo) == 1
    step_info = step_information_repo.get(step_keyword, step_name)
    assert step_info is not None
    step_information_repo.repo.remove(step_info)  # Clean the repository after the test
    assert step_info.step_keyword == step_keyword
    assert step_info.step_name == step_name
    assert step_info.json != []
    assert len(step_info.json) == len(json_informations)
    for json_info in json_informations:
        formatted_json_info = json.dumps(json_info, indent=2).strip()
        assert formatted_json_info in step_info.json


def test_attach_empty_text_to_step():
    step_keyword = "Given"
    step_name = "Step name"
    attach.text_to_step("", step_keyword, step_name)

    assert len(step_information_repo.repo) == 0
    step_info = step_information_repo.get(step_keyword, step_name)
    assert step_info is None


def test_attach_empty_json_to_step():
    step_keyword = "Given"
    step_name = "Step name"
    attach.json_to_step({}, step_keyword, step_name)

    assert len(step_information_repo.repo) == 0
    step_info = step_information_repo.get(step_keyword, step_name)
    assert step_info is None


def test_attach_text_and_json_to_step():
    step_keyword = "Given"
    step_name = "Step name"
    text_info = "Test information"
    json_info = {"test": "information"}
    formatted_json_info = json.dumps(json_info, indent=2).strip()

    attach.text_to_step(text_info, step_keyword, step_name)
    attach.json_to_step(json_info, step_keyword, step_name)

    assert len(step_information_repo.repo) == 1
    step_info = step_information_repo.get(step_keyword, step_name)
    assert step_info is not None
    step_information_repo.repo.remove(step_info)  # Clean the repository after the test
    assert step_info.step_keyword == step_keyword
    assert step_info.step_name == step_name
    assert step_info.json != []
    assert step_info.text != []
    assert formatted_json_info in step_info.json
    assert text_info in step_info.text


@given(
    text_informations=st.lists(elements=st.text(min_size=1), min_size=1),
    json_informations=st.lists(
        elements=st.dictionaries(
            keys=st.text(min_size=1),
            values=st.text(min_size=1),
            min_size=1,
        ),
        min_size=1,
    ),
)
def test_attach_multiple_text_and_json_to_step(
    text_informations: list[str], json_informations: list[dict]
):
    step_keyword = "Given"
    step_name = "Step name"

    for text_info in text_informations:
        attach.text_to_step(text_info, step_keyword, step_name)

    for json_info in json_informations:
        attach.json_to_step(json_info, step_keyword, step_name)

    assert len(step_information_repo.repo) == 1
    step_info = step_information_repo.get(step_keyword, step_name)
    assert step_info is not None
    step_information_repo.repo.remove(step_info)  # Clean the repository after the test
    assert step_info.step_keyword == step_keyword
    assert step_info.step_name == step_name
    assert len(step_info.text) == len(text_informations)
    for text_info in text_informations:
        assert text_info in step_info.text
    assert len(step_info.json) == len(json_informations)
    for json_info in json_informations:
        formatted_json_info = json.dumps(json_info, indent=2).strip()
        assert formatted_json_info in step_info.json
