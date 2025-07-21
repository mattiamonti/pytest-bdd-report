import pytest
from tests.bdd.fixtures.setup_fixtures import *
import uuid

@pytest.fixture
def get_uuid():
    def _generate():
        return str(uuid.uuid4()).replace("-","")[:8]
    return _generate