import shutil
import os
import pytest


@pytest.fixture()
def cleanup_bdd_generated():
    # Setup (se necessario)
    yield
    # Teardown
    folder = "generated_tests"
    if os.path.exists(folder) and os.path.isdir(folder):
        shutil.rmtree(folder)
    report = "proto_bdd_testing.html"
    if os.path.exists(report) and os.path.isfile(report):
        os.remove(report)
    
