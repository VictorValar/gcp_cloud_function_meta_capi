import json
import pytest

@pytest.fixture(scope='module')
def json_payload():
    with open('app/tests/test_event.json', 'r') as file:
        json_payload = json.load(file)

    yield json_payload