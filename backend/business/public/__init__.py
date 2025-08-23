from flask import Blueprint

business_public_bp = Blueprint("business_public_bp", __name__, url_prefix="")

from backend.auth.auth_checks import login_required

from . import routes
