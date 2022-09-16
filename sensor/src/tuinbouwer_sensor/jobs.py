"""Jobs for scheduler module"""

from tuinbouwer_sensor import application


def send_log_information():
    """job for sending log information"""
    application.send_log_information()
