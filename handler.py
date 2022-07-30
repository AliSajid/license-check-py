import datetime
import logging
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    ip_address = requests.get('http://checkip.amazonaws.com').text
    logger.info("Your cron function " + name + " ran at " + str(current_time) + " from " + ip_address)

def check_license(event, context):
    url = "https://dlims.punjab.gov.pk/track/"

    response = requests.get(url)
    if response.status_code == 200:
        logger.info("License is valid")
    else:
        logger.info("License is invalid")
        return False