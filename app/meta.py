import logging
import os
from facebook_business.adobjects.serverside.event_request import EventRequest
from facebook_business.adobjects.serverside.event_response import EventResponse
from facebook_business.api import FacebookAdsApi
from dotenv import load_dotenv, find_dotenv

def send_events(events: list) -> EventResponse:
    """
    Sends events to Meta Ads
    """
    load_dotenv(find_dotenv())
    PIXEL_ID = int(os.getenv('PIXEL_ID'))
    PIXEL_ACCESS_TOKEN = os.getenv('PIXEL_ACCESS_TOKEN')
    TEST_EVENT_CODE = os.getenv('TEST_EVENT_CODE')
    ENV = os.getenv('ENV')

    FacebookAdsApi.init(access_token=PIXEL_ACCESS_TOKEN)

    if ENV in ['dev', 'testing']:
        event_request = EventRequest(
            events=events,
            pixel_id=str(PIXEL_ID),
            test_event_code=TEST_EVENT_CODE,
            access_token=PIXEL_ACCESS_TOKEN
        )
    else:
        event_request = EventRequest(
            events=events,
            pixel_id=str(PIXEL_ID),
            access_token=PIXEL_ACCESS_TOKEN
        )

    event_response = event_request.execute()
    logging.info(f'##### Purchase event sent to meta: {event_response}')

    return event_response
