from flask import Blueprint, request, jsonify, current_app

s3_storage_bp = Blueprint("storage", __name__, url_prefix="/storage")

from . import routes