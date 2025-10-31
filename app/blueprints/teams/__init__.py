from flask import Blueprint

teams_bp = Blueprint('teams_bp', __name__)

from . import routes