from flask import Blueprint, jsonify, url_for, redirect, render_template, request, session
from supabase_client import supabase
from postgrest.exceptions import APIError
from functools import wraps
from . import tanuAdmin_bp

# Function Description: Checks if user is an admin

def admin_account_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ui = session["supabase_user"]
        if ui["google_email"] != "ttaribi@terpmail.umd.edu":
            return redirect(url_for("auth_bp.login"))
        return f(*args, **kwargs)
    return decorated

# Function Description: Retrieves current business forms from db and sends to front end

@tanuAdmin_bp.route("/admin")
@admin_account_required
def admin_portal():
    try:
        resp = supabase.table("BusinessAccountRequests").select("*").execute()
        requests = resp.data if resp.data else []
    except Exception as e:
        requests = []
    return render_template("admin_portal.html", requests=requests)
