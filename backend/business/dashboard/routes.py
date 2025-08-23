import requests
from flask import Blueprint, redirect, request, render_template, session, url_for, jsonify
from backend.clients import supabase
from postgrest.exceptions import APIError
from . import business_dash_bp
from backend.auth.auth_checks import login_required

@login_required
@business_dash_bp.route('/')
def business_profile():
    user_id = session['supabase_user']['id']
    resp = supabase.table("Businesses").select("*").eq("owner_id", user_id).maybe_single().execute()

    if resp:
        resp = resp.data

    return render_template("business_profile.html", business=resp)

    