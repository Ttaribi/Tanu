from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="")

# re-export login_required and any other helpers
from .auth import login_required
# and of course import your routes so they get registered on auth_bp
from .auth import *  
