import os
import json
from hypothesis import given, strategies as st
from pytest_bdd_report.loader.json_loader import JsonLoader

TEST_DATA_FILE = "tests/data/mock_json.json"


def clear_file():
    os.remove(TEST_DATA_FILE)


def save_json_file(data):
    test_data_file = "tests/data/mock_json.json"
    with open(test_data_file, "w") as f:
        json.dump(data, f)


@given(data=st.dictionaries(st.text(min_size=1), st.text()))
def test_loading_json(data):
    save_json_file(data)

    loaded_data = JsonLoader(TEST_DATA_FILE).load()

    assert loaded_data == data
    clear_file()
