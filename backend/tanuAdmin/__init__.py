from flask import Blueprint

tanuAdmin_bp = Blueprint("tanuAdmin_bp", __name__, url_prefix="/tanuAdmin")

from . import tanuAdmin