from flask import Blueprint

business_dash_bp = Blueprint("business_dash_bp", __name__, url_prefix="/dashboard/business")

from backend.auth.auth_checks import login_required

from . import routes
