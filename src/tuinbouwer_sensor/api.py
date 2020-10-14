"""API module"""

import time

import requests

from tuinbouwer_sensor import BASE_URL, HEADERS


def post_sensor_log(sensor_log):
    """Download item id"""
    tries = 1
    html = ''
    while not html and tries <= 3:
        response = requests.post(
            '{}'.format(BASE_URL),
            headers=HEADERS,
            data=sensor_log,
        )
        if html:
            html = response.text
        else:
            time.sleep(5)
            tries += 1
    return html
