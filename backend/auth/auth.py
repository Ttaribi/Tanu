import requests
from flask import Blueprint, redirect, request, render_template, session, url_for, jsonify
from supabase_client import supabase
from postgrest.exceptions import APIError
from functools import wraps
from . import auth_bp


auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route('/')
def home():
    return redirect(url_for('auth_bp.login'))

# Gets us the Google sign in url which we load up in the user's current page
@auth_bp.route("/login", methods=["GET"])
def login():
    # is what we will redirect to after user logs in
    callback = url_for("auth_bp.auth_callback", _external=True)
    # Build the params dict whichs holds info for supabase to handle login
    params = {

        "provider": "google",
        "options": {"redirect_to": callback}
    }
    # Supabase gives us our Google path URL based on the param dictionary we fed it
    oauth_response = supabase.auth.sign_in_with_oauth(params)

    # Return that url for user to login in
    return redirect(oauth_response.url)



# OAUTH CALLBACK: Handle Supabase + Google’s response
@auth_bp.route("/auth/callback")
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


    if not user.email.endswith("@terpmail.umd.edu"):
        supabase.auth.sign_out()

        # Lets you attempt again to use terpmail
        return redirect(url_for("auth_bp.login"))
    
    # We store our user info from our supabase session in our flask sessino
    session["supabase_user"] = {"auth_id": user.id, "google_email": user.email, }
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
    exists = supabase.table("UserAccounts").select("*").eq("auth_id", user.id).execute().data
    if exists:
        return redirect(url_for("dashboard_bp.dashboard"))
    return redirect(url_for("auth_bp.complete_profile"))

    

'''
Purpose: Protect certain auth_bp so that only logged in users can access them.
It checks if we stored "supabase_user" in Flask’s session
If not, it redirects to the /login route. Otherwise it lets the original function run.
'''

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "supabase_user" not in session:
            return redirect(url_for("auth_bp.login"))
        return f(*args, **kwargs)
    return decorated


# Completes the Prfile: show form (GET) & save alt_email (POST)
@auth_bp.route("/complete_profile", methods=["GET","POST"])
@login_required
def complete_profile():
    
    ui = session["supabase_user"]

    #If the request is get, indicates we need retrieve the prfoile
    if request.method == "GET":
        return render_template("complete_profile.html", email=ui["google_email"])


    alt = request.form.get("alt_email", "").strip() or None
    first_name = request.form.get("first_name", "").strip() or None
    last_name = request.form.get("last_name", "").strip() or None

    # Resp holds a response from supabase which hold the data, error code, and more
    try:
        resp = (supabase
            .table("UserAccounts")
            .upsert({
                "auth_id":      ui["auth_id"],
                "google_email": ui["google_email"],
                "alt_email":    alt,
                "first_name":   first_name,
                "last_name":    last_name

            }, on_conflict=["auth_id"])
            .execute()
        )


        '''
        in Memory

            {
            "auth_id": "12345",
            "google_email": "student@umd.edu",
            "alt_email": "alt@gmail.com",
            "first_name": "Ta",
            "last_name": "nu"
            }
 
        
        '''
    except APIError as e:
        return jsonify({"error": str(e)}), 500

    return redirect(url_for("dashboard_bp.dashboard"))



@auth_bp.route("/skip_profile")
@login_required
def skip_profile():
    ui = session["supabase_user"]

    try:
        resp = (supabase
            .table("UserAccounts")
            .upsert({
                "auth_id":      ui["auth_id"],
                "google_email": ui["google_email"],
                "alt_email":    None
            }, on_conflict=["auth_id"])
            .execute()
        )
    except APIError as e:
        return jsonify({"error": str(e)}), 500

    return redirect(url_for("auth_bp.profile"))


@auth_bp.route('/logout')
def logout():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    
    session.clear()
    return redirect(url_for("auth_bp.home"))