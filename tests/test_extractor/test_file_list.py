import pytest
from hypothesis import given
from hypothesis import strategies as st

from pytest_bdd_report.extractor.file_list import FileListRepo


@pytest.fixture
def file_list_repo():
    return FileListRepo()


@given(
    filename=st.text(min_size=1),
)
def test_add_and_get_file_in_list(filename: str):
    file_list_repo = FileListRepo()

    file_list_repo.add(filename)

    file_list = file_list_repo.get()
    assert len(file_list) == 1
    assert file_list[0] == filename


def test_add_multiple_files(file_list_repo: FileListRepo):
    file_1 = "dir/file_1.py"
    file_2 = "dir/file_2.py"
    file_3 = "dir/file_3.py"

    file_list_repo.add(file_1)
    file_list_repo.add(file_2)
    file_list_repo.add(file_3)

    file_list = file_list_repo.get()
    assert len(file_list) == 3
    assert file_list[0] == file_1
    assert file_list[1] == file_2
    assert file_list[2] == file_3


@given(
    filename=st.text(min_size=1),
)
def test_should_not_add_same_files(filename: str):
    file_list_repo = FileListRepo()

    file_list_repo.add(filename)
    file_list_repo.add(filename)

    file_list = file_list_repo.get()
    assert len(file_list) == 1
    assert file_list[0] == filename


@given(
    filename=st.text(min_size=0, max_size=0),
)
def test_should_not_add_empty_file_name(filename: str):
    file_list_repo = FileListRepo()

    file_list_repo.add(filename)

    file_list = file_list_repo.get()
    assert len(file_list) == 0
