import requests
from flask import Blueprint, redirect, request, render_template, session, url_for, jsonify
from supabase_client import supabase, SUPABASE_URL, SUPABASE_KEY
from postgrest.exceptions import APIError
from functools import wraps


routes = Blueprint("routes", __name__)

@routes.route('/')
def home():
    return redirect(url_for('routes.login'))

#1) Entry point: Kicks off the OAuth flow
@routes.route("/login", methods=["GET"])
def login():
    # is what we will redirect to after user logs in
    callback = url_for("routes.auth_callback", _external=True)
    # Build the params dict whichs holds info for supabase to handle login
    params = {
        "provider": "google",
        "options": {"redirect_to": callback}
    }
    # Supabase gives us our Google path URL based on the param dictionary we fed it
    oauth_response = supabase.auth.sign_in_with_oauth(params)

    # Return that url for user to login in
    return redirect(oauth_response.url)





# 2) OAUTH CALLBACK: Handle Supabase + Google’s response
@routes.route("/auth/callback")
def auth_callback():
    #Google returns to us a code which indicates whther login is successful or not
    #If no code, it wasnt successful and no login occured
    code = request.args.get("code")
    if not code:
        return "No authorization code provided", 400

    # We use our code to exchange for a supabase sessino
    try:
        auth_response = supabase.auth.exchange_code_for_session({"auth_code": code})
    except Exception as e:
        return f"Session exchange failed: {e}", 400

    # Extract the session and get user info
    #    In supabase py v2, auth_response.session is a GotrueSession
    sess = auth_response.session
    user = sess.user
    access_token = sess.access_token

    #Enforce UMD email
    if not user.email.endswith("@terpmail.umd.edu"):
        supabase.auth.sign_out()
        # Lets you attempt again to use terpmail
        return redirect(url_for("routes.login"))
    
    # We store our user info from our supabase session in our flask sessino
    session["supabase_user"] = {"id": user.id, "email": user.email}
    session["supabase_access_token"] = access_token

    '''
    This looks like this in memory 

    session = {
    "supabase_user": {
        "id": "12345-abcde",              # <- Supabase user ID
        "email": "student@terpmail.umd.edu"  # <- Supabase email
    },
    "supabase_access_token": "eyJhbGciOi..."  # <- JWT access token
}
    '''

    # We check whether a profile already exists and redirect from there
    exists = supabase.table("authTablePrac").select("*").eq("auth_id", user.id).execute().data
    if exists:
        return redirect(url_for("routes.profile"))
    return redirect(url_for("routes.complete_profile"))

    

'''
Purpose: Protect certain routes so that only logged in users can access them.
It checks if we stored "supabase_user" in Flask’s session
If not, it redirects to the /login route. Otherwise it lets the original function run.
'''
# Protect all “logged in only” routes
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "supabase_user" not in session:
            return redirect(url_for("routes.login"))
        return f(*args, **kwargs)
    return decorated


# Completes the Prfile: show form (GET) & save alt_email (POST)
@routes.route("/complete_profile", methods=["GET","POST"])
@login_required
def complete_profile():
    # Gets user info form session
    ui = session["supabase_user"]

    #If the request is get, indicates we need retrieve the prfoile
    if request.method == "GET":
        return render_template("complete_profile.html", email=ui["email"])

    #Means we need to finish the profile creation
    alt = request.form.get("alt_email", "").strip() or None
    # Resp holds a response from supabase which hold the data, error code, and more
    try:
        resp = (supabase
            .table("authTablePrac")
            .upsert({
                "auth_id":      ui["id"],
                "google_email": ui["email"],
                "alt_email":    alt
            }, on_conflict=["auth_id"])
            .execute()
        )

        '''
        in Memory

            {
            "auth_id": "12345",
            "google_email": "student@umd.edu",
            "alt_email": "alt@gmail.com"
            }

        
        '''
    except APIError as e:
        return jsonify({"error": str(e)}), 500

    return redirect(url_for("routes.profile"))


# To skip alt email
@routes.route("/skip_profile")
@login_required
def skip_profile():
    ui = session["supabase_user"]

    try:
        resp = (supabase
            .table("authTablePrac")
            .upsert({
                "auth_id":      ui["id"],
                "google_email": ui["email"],
                "alt_email":    None
            }, on_conflict=["auth_id"])
            .execute()
        )
    except APIError as e:
        return jsonify({"error": str(e)}), 500

    return redirect(url_for("routes.profile"))


# 4) PROFILE: show the user’s saved profile
@routes.route("/profile", methods=["GET"])
@login_required
def profile():
    ui = session["supabase_user"]

    try:
        resp = (supabase
            .table("authTablePrac")
            .select("*")
            .eq("auth_id", ui["id"])
            .single()
            .execute()
        )
        # Resp holds a response object returned from supabase after a query.
    except APIError as e:
        return jsonify({"error": str(e)}), 500

    
    return jsonify({
        "user":    ui,
        "profile": resp.data
    }), 200

