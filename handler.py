import datetime
import logging
import requests
from bs4 import BeautifulSoup
from os import environ
from fake_headers import Headers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    ip_address = requests.get('http://checkip.amazonaws.com').text
    logger.info("Your cron function " + name + " ran at " +
                str(current_time) + " from " + ip_address)


def check_license(event, context):
    url = "https://dlims.punjab.gov.pk/track/"
    cnic = environ.get('CNIC', "0000000000000")

    payload = {"trackbynumber": cnic}

    headers = Headers(headers=True)

    response = requests.post(url, data=payload, headers=headers.generate())

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        elem = soup.select(
            "#content > div.big-title.text-center.animated.fadeInDown.delay-01 > h1")
        if elem:
            status = elem[0].string
            logger.info(f"Response from website: {elem[0].string}")
            if status == "Your regular license is in printing queue.":
                logger.info("Your license is in printing queue")
                return True
            else:
                logger.info("Your license is not in printing queue")
                return True

        else:
            logger.error(f"No response from website")
        return False
    else:
        logger.error("Call to check license failed")
        return False
