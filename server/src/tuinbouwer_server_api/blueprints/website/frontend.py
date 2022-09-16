"""Website blueprint"""

from flask import Blueprint, abort, request

blueprint = Blueprint('website', __name__, url_prefix='/')

@blueprint.route('/', methods=(['GET']))
def index():
    """Index page"""
    return "Welcome"

@blueprint.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return abort(404)
