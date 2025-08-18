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
