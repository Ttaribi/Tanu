from flask import Blueprint


student_profile_bp = Blueprint('student_profile_bp', __name__, url_prefix='/student_profile')

from . import student_profile         
