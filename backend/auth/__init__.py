from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="")

# We. get the login_route decarator from our auth file
from .auth import login_required
# Imports our routes so they get registered on auth_bp
from .auth import *  
