from flask import Blueprint

user_profile_bp = Blueprint("user_profile_bp", __name__, url_prefix="/profile")

from . import user_profile