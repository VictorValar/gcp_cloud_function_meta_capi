import logging
from facebook_business.adobjects.serverside.user_data import UserData
from facebook_business.adobjects.serverside.content import Content
from facebook_business.adobjects.serverside.custom_data import CustomData
from facebook_business.adobjects.serverside.event import Event
from facebook_business.adobjects.serverside.action_source import ActionSource
from . import meta

def event_handler(payload):
    """
    Sends events to Facebook Ads
    """

    if not payload.get('user_data').get('user_id'):
        logging.error('##### No user_id found in payload')
        raise ValueError('No user_id found in payload')


    user_data = UserData(
        external_id=payload.get('user_data').get('user_id'),
    )

    items = payload.get('items')
    contents = []

    for item in items:
        content = Content(
            product_id=item.get('id'),
            quantity=item.get('quantity'),
            item_price=item.get('price'),
            brand=item.get('item_brand'),
            title=item.get('item_name'),
            category=item.get('item_category')
        )
        contents.append(content)

    custom_data = CustomData(
        contents=contents,
        content_type='product',
        currency='BRL',
        value=payload.get('user_data').get('transaction_value'),
        order_id=payload.get('user_data').get('transaction_id'),
        custom_properties={'payment_type': payload.get('user_data').get('payment_type')}

    )

    event = Event(
        event_name='Purchase',
        event_time=int(payload.get('user_data').get('transaction_time')),
        user_data=user_data,
        custom_data=custom_data,
        action_source=ActionSource.SYSTEM_GENERATED,
        event_id=payload.get('user_data').get('transaction_id'),
    )

    return meta.send_events([event])