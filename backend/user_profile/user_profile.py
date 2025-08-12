from flask import Blueprint, session, url_for, render_template, redirect
from backend.clients import supabase
from backend.auth.auth import login_required
from . import user_profile_bp

@user_profile_bp.route("/user_profile")
@login_required
def user_profile():

    ui = session["supabase_user"]

    return render_template("user_profile.html", user = ui)