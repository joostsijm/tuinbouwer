"""API module"""

import time

import requests

from tuinbouwer_sensor import BASE_URL, HEADERS, LOGGER


def post_sensor_log(sensor_log):
    """Download item id"""
    tries = 1
    html = ''
    while not html and tries <= 3:
        try:
            response = requests.post(
                '{}'.format(BASE_URL),
                headers=HEADERS,
                data=sensor_log,
            )
        except requests.exceptions.ConnectionError as error:
            LOGGER.error(error)
            LOGGER.info("Trying again to POST sensor log")
        if response:
            html = response.text
        else:
            time.sleep(5)
            tries += 1
    return html
