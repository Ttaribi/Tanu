from flask import Blueprint


user_settings_bp = Blueprint('user_settings_bp', __name__, url_prefix='/user_settings')

from . import user_settings    
