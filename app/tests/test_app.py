from ..app import event_handler
import pytest
def test_main_returns_1_event_received(json_payload):
    response = event_handler(json_payload)
    assert response.events_received == 1

def test_no_user_id(json_payload):
    """
    Test if the function raises an exception when no user_id is found in the payload
    """
    del json_payload['user_data']['user_id']
    with pytest.raises(ValueError):
        event_handler(json_payload)

