import logging
import time
import os
from flask import request
from facebook_business.adobjects.serverside.action_source import ActionSource
from facebook_business.adobjects.serverside.content import Content
from facebook_business.adobjects.serverside.custom_data import CustomData
from facebook_business.adobjects.serverside.delivery_category import DeliveryCategory
from facebook_business.adobjects.serverside.event import Event
from facebook_business.adobjects.serverside.event_request import EventRequest
from facebook_business.adobjects.serverside.user_data import UserData
from facebook_business.api import FacebookAdsApi
from dotenv import load_dotenv, find_dotenv
import random


# Settings
PIPE_IP_FIELD_ID = '5cf007272df34771337bb802f663d7bb89bb87df'
PIPE_USER_AGENT_FIELD_ID = '5fc3af8ff260dd3428f12b32120e67dbb911f974'
PIPE_FBC_FIELD_ID = '0d4c458a1201db3824a7edce90698838ea715b0e'
PIPE_FBP_FIELD_ID = '91865ac47801649d827eb3562116486a733577be'


def send_event(deal: object, event_name: str, lead_score: int):
    """
    Sends a event to Meta Ads
    """

    PIXEL_ID = int(os.getenv('PIXEL_ID'))
    PIXEL_ACCESS_TOKEN = os.getenv('PIXEL_ACCESS_TOKEN')
    TEST_EVENT_CODE = os.getenv('TEST_EVENT_CODE')
    ENV = os.getenv('ENV')

    FacebookAdsApi.init(access_token=PIXEL_ACCESS_TOKEN)

    user_data = set_user_data(deal=deal)

    # user_data = UserData(
    #     emails=emails,
    #     phones=phones,
    #     fbc=deal['data']['0d4c458a1201db3824a7edce90698838ea715b0e'],
    #     # It is recommended to send Client IP and User Agent for Conversions API Events.
    #     client_ip_address=request.META.get('REMOTE_ADDR'),
    #     client_user_agent=request.headers['User-Agent'],
    #     fbp='fb.1.1558571054389.1098115397',
    # )

    # content = Content(
    #     product_id='product123',
    #     quantity=1,
    #     delivery_category=DeliveryCategory.HOME_DELIVERY,
    # )

    custom_data = CustomData(
        # contents=[content],
        currency='brl',
        value=lead_score if event_name.lower() != 'purchase'else deal.get('data').get('value')*0.005,
        custom_properties={'lead_score': lead_score}

    )

    event = Event(
        event_name=event_name,
        event_time=int(time.time()),
        user_data=user_data,
        custom_data=custom_data,
        action_source=ActionSource.SYSTEM_GENERATED,
        event_id=str(random.randint(0, 999999999999)),
        # event_source_url='http://jaspers-market.com/product/123',
    )

    events = [event]

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
    logging.info(f'##### {event_name} event sent to meta: {event_response}')

    return event_response


def set_user_data(deal: object) -> UserData:
    """
    Instantiates UserData depending on available user fields
    """

    emails = []
    phones = []

    person = deal.get('related_objects').get('person')

    try:
        for i in person.keys():
            for email in person[i]['email']:
                emails.append(email['value'])

            for phone in person[i]['phone']:
                phones.append(phone['value'])
    except Exception:
        pass

    ip_address_field = deal.get('data').get(PIPE_IP_FIELD_ID)
    user_agent_field = deal.get('data').get(PIPE_USER_AGENT_FIELD_ID)
    fbc_field = deal.get('data').get(PIPE_FBC_FIELD_ID)
    fbp_field = deal.get('data').get(PIPE_FBP_FIELD_ID)

    user_data = UserData(
        emails=emails,
        phones=phones,
        )

    if ip_address_field not in [None, "", " "]:
        user_data.client_ip_address = ip_address_field

    if user_agent_field not in [None, "", " "]:
        user_data.client_user_agent = user_agent_field

    if fbc_field not in [None, "", " "]:
        if fbc_field[0:3] == 'fb.':
            user_data.fbc = fbc_field

    if fbp_field not in [None, "", " "]:
        if fbp_field[0:3] == 'fb.':
            user_data.fbp = fbp_field


    # logs found user data
    # logging.info(f'User Data: {user_data}')
    return user_data
