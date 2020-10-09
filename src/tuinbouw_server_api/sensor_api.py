"""Page blueprint"""

import os
from smtplib import SMTPServerDisconnected

from flask import Blueprint, redirect, url_for, abort


sensor_api = Blueprint('sensor_api', __name__, url_prefix='/sensor_api/v1')

@sensor_api.route('/', methods=(['POST']))
def contact():
    """Route to POST sensor data"""

@sensor_api.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return abort(404)
