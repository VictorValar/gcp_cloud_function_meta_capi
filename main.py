import functions_framework
import logging
import traceback
import json
from app.app import event_handler
@functions_framework.http
def main(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    logging.debug(msg='funcall: lambda_handler')
    payload = request_json
    logging.info(msg=f'payload: {json.dumps(payload, indent=4, sort_keys=True)}')

    try:
        response = event_handler(payload)
        logging.info(msg=f'response: {json.dumps(response, indent=4, sort_keys=True)}')
        return response

    except Exception as excp:
        traceback.print_exc()
        logging.error(excp)
        return {
            'statusCode': 400 if type(excp) == ValueError else 500,
            'body': f'event not sent: {str(excp)} {str(traceback.format_exc())}',
        }


