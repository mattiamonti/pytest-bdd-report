import json

import pytest
from hypothesis import given
from hypothesis import strategies as st

from pytest_bdd_report import attach
from pytest_bdd_report.extensions.step_information import step_information_repo
from tests.test_report_creation.fixtures import sample_test_with_step_attachments


@given(
    step_keyword=st.sampled_from(["Given", "When", "And", "Then"]),
    step_name=st.text(min_size=1),
    text_information=st.text(min_size=1),
)
def test_attach_text_to_step(step_keyword: str, step_name: str, text_information: str):
    attach.text_to_step(text_information, step_keyword, step_name)

    assert len(step_information_repo.repo) == 1
    step_info = step_information_repo.get(step_keyword, step_name)
    assert step_info is not None
    step_information_repo.repo.clear()
    assert step_info.step_keyword == step_keyword
    assert step_info.step_name == step_name
    assert step_info.text != []
    assert step_info.text[0] == text_information
    assert step_info.json == []


@given(
    step_keyword=st.sampled_from(["Given", "When", "And", "Then"]),
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
    step_information_repo.repo.clear()
    assert step_info.step_keyword == step_keyword
    assert step_info.step_name == step_name
    assert step_info.text != []
    assert len(step_info.text) == len(text_informations)
    for text_info in text_informations:
        assert text_info in step_info.text


@given(
    step_keyword=st.sampled_from(["Given", "When", "And", "Then"]),
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
    step_information_repo.repo.clear()
    assert step_info.step_keyword == step_keyword
    assert step_info.step_name == step_name
    assert step_info.json != []
    assert step_info.json[0] == formatted_json_information
    assert step_info.text == []


@given(
    step_keyword=st.sampled_from(["Given", "When", "And", "Then"]),
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
    step_information_repo.repo.clear()
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
    step_information_repo.repo.clear()
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
    step_information_repo.repo.clear()
    assert step_info.step_keyword == step_keyword
    assert step_info.step_name == step_name
    assert len(step_info.text) == len(text_informations)
    for text_info in text_informations:
        assert text_info in step_info.text
    assert len(step_info.json) == len(json_informations)
    for json_info in json_informations:
        formatted_json_info = json.dumps(json_info, indent=2).strip()
        assert formatted_json_info in step_info.json


def test_add_unregistered_data_to_step_information_repo():
    step_keyword = "Given"
    step_name = "Step name"
    unregistered_list_info = ["first", "second"]

    with pytest.raises(RuntimeWarning):
        step_information_repo.add(step_keyword, step_name, unregistered_list_info)

    assert len(step_information_repo.repo) == 0


def test_creation_with_step_attachments(
    sample_test_with_step_attachments: pytest.Testdir,
):
    sample_test_with_step_attachments.runpytest("--bdd-report=with_attachments")
    report_file = sample_test_with_step_attachments.tmpdir / "with_attachments.html"
    with open(report_file, "r") as f:
        content = f.read()
        assert "Test text attachment" in content
    assert report_file.exists()


@given(
    step_keyword_1=st.sampled_from(["Given", "When", "And", "Then"]),
    step_name_1=st.text(min_size=1),
    text_1=st.text(min_size=1),
    step_keyword_2=st.sampled_from(["Given", "When", "And", "Then"]),
    step_name_2=st.text(min_size=1),
    text_2=st.text(min_size=1),
)
def test_isolation(
    step_keyword_1: str,
    step_name_1: str,
    text_1: str,
    step_keyword_2: str,
    step_name_2: str,
    text_2: str,
):
    step_information_repo.repo.clear()
    if step_name_1 == step_name_2:
        return

    attach.text_to_step(text_1, step_keyword_1, step_name_1)
    attach.text_to_step(text_2, step_keyword_2, step_name_2)
    assert len(step_information_repo.repo) == 2
    step_info_1 = step_information_repo.get(step_keyword_1, step_name_1)
    step_info_2 = step_information_repo.get(step_keyword_2, step_name_2)
    assert step_info_1 is not None
    assert step_info_2 is not None
    step_information_repo.repo.clear()
    assert step_info_1.step_keyword == step_keyword_1
    assert step_info_1.step_name == step_name_1
    assert text_1 in step_info_1.text
    assert step_info_2.step_keyword == step_keyword_2
    assert step_info_2.step_name == step_name_2
    assert text_2 in step_info_2.text
