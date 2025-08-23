from flask import render_template, session
from auth.auth_checks import login_required   
from . import dashboard_bp

@dashboard_bp.route("/")
#@login_required
def dashboard():
    
    return render_template("dashboard_new.html")

