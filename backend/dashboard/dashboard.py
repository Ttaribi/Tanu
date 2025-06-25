from flask import render_template, session
from auth import login_required   # <-- import from auth package
from . import dashboard_bp

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    user = session["supabase_user"]
    return render_template("dashboard.html", user=user)

@dashboard_bp.route("/settings")
@login_required
def settings():
    return render_template("settings.html")
