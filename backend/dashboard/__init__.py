from flask import Blueprint

dashboard_bp = Blueprint("dashboard_bp", __name__, url_prefix="")

# This imports the view functions so they register on dashboard_bp
from .dashboard import *
