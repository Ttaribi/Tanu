from flask import Blueprint

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="")

# import your view functions so they register on dashboard_bp
from .dashboard import *
