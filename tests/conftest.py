import pytest
import copy
from fastapi.testclient import TestClient
from src import app as fastapi_app, app

@pytest.fixture(autouse=True)
def reset_activities():
    # Deepcopy the original activities dict
    orig = copy.deepcopy(app.activities)
    yield
    # Restore activities to original state
    app.activities.clear()
    app.activities.update(orig)

@pytest.fixture
def client():
    return TestClient(fastapi_app.app)
