from flask import Blueprint

runners_bp = Blueprint('runners_bp', __name__)

from . import routes