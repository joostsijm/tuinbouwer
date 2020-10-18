"""Markt Controle voor Onderzoek en Analyse"""

import os
import logging

from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler


load_dotenv()

# scheduler
SCHEDULER = BackgroundScheduler(
    daemon=True,
    job_defaults={'misfire_grace_time': 5*60},
    max_instances=5,
)
SCHEDULER.start()

# get logger
LOGGER = logging.getLogger('tuinbouwer_sensor')
LOGGER.setLevel(logging.DEBUG)
SCHEDULER_LOGGER = logging.getLogger('apscheduler')
SCHEDULER_LOGGER.setLevel(logging.DEBUG)

# create file handler
FILE_HANDLER = logging.FileHandler('output.log')
FILE_HANDLER.setLevel(logging.DEBUG)

# create console handler
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(logging.INFO)

# create formatter and add it to the handlers
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
STREAM_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setFormatter(FORMATTER)

# add the handlers to logger
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(FILE_HANDLER)
SCHEDULER_LOGGER.addHandler(STREAM_HANDLER)
SCHEDULER_LOGGER.addHandler(FILE_HANDLER)

# api
BASE_URL = os.environ.get('API_URL', None)
HEADERS = {
    'Authorization': os.environ.get('AUTHORIZATION', 'http://localhost:5000/')
}
