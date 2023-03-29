"""Website blueprint"""

from flask import Blueprint, abort, request, send_file, send_from_directory


blueprint = Blueprint('website', __name__, url_prefix='/')

@blueprint.route('/', methods=(['GET']))
def index():
    """Index page"""
    return send_file('frontend/index.html')

@blueprint.route('/favicon.ico', methods=(['GET']))
def favicon():
    return send_file('frontend/favicon.ico')

@blueprint.route('/js/<path:path>', methods=(['GET']))
def send_js(path):
    return send_from_directory('frontend/js/', path)

@blueprint.route('/css/<path:path>', methods=(['GET']))
def send_css(path):
    return send_from_directory('frontend/css/', path)

@blueprint.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return abort(404)
