from flask import Blueprint

session_bp = Blueprint('session', __name__, url_prefix='/session', template_folder='../../templates')

from . import routes
