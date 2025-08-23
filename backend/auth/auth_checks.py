from flask import redirect, url_for, session, render_template
from functools import wraps

'''
Purpose: Protect certain auth_bp so that only logged in users can access them.
It checks if we stored "supabase_user" in Flask’s session
If not, it redirects to the /login route. Otherwise it lets the original function run.
'''

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "supabase_user" not in session:
            return render_template("login.html")
        return f(*args, **kwargs)
    return decorated


# Function Description: Checks user's role to allow/deny access
def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            ui = session["supabase_user"]
            if ui['role'] not in roles:
                return ({"Access Denied": "Forbidden role"})
            return f(*args, **kwargs)
        return decorated
    return wrapper


