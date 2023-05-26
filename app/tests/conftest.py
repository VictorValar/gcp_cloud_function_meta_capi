import json

@pytest.fixture(scope='module')
def json_payload():
    with open('test_event.json', 'r') as file:
        json_payload = json.load(file)

    yield json_payload