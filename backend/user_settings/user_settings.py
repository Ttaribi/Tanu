from flask import redirect, url_for, render_template, session, request, jsonify
from backend.clients import supabase
from backend.auth.auth import login_required
from . import user_settings_bp

# Function Summary: This functinos retrieves info from supabase so we can load up the page
#                   with the current user's info
@user_settings_bp.route("", methods=["GET"])
@user_settings_bp.route("/", methods=["GET"])
@login_required
def user_settings():
    ui = session["supabase_user"]

    
    supabase.table("UserAccounts").upsert({
        "auth_id":      ui["auth_id"],
        "google_email": ui["google_email"],
    }, on_conflict=["auth_id"]).execute()

   
    profile = (
        supabase
          .table("UserAccounts")
          .select("*")
          .eq("auth_id", ui["auth_id"])
          .single()
          .execute()
          .data
    )
    session["supabase_user"] = profile
    return render_template("user_settings.html", user=profile)


# Function Summary: This function helps update the user's alt email by checking if it is valid
#                   then upserts new email into supabase
@user_settings_bp.route('/update-alt-email', methods=['POST'])
@login_required
def update_alt_email():
    data = request.get_json() or {}
    new_alt = data.get('alt_email', '').strip()

    if not new_alt:
        return jsonify(success=False, message="Email cannot be empty"), 400

    ui = session["supabase_user"]
    try:
        resp = (
          supabase
          .table("UserAccounts")
          .upsert(
            {
              "auth_id":   ui["auth_id"],
              "alt_email": new_alt
            },
            on_conflict="auth_id"
          )
          .execute()
        )
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

    
    if not resp.data:
        return jsonify(success=False,
                       message="No row was inserted or updated"), 500


    session["supabase_user"]["alt_email"] = new_alt

    return jsonify(success=True, message="Alternative email updated successfully")


#Function Description: This functino handles retrieving info from the current user

@user_settings_bp.route('/create-business-account', methods=['GET'])
@login_required
def create_business_account_form():
    ui = session.get("supabase_user")
    return render_template('create_business_account.html', user=ui)

#Function Description: This function takes info from the javascript so we can
#                      add it to our supabase db
@user_settings_bp.route('/create-business-account', methods=['POST'])
@login_required
def create_business_account_submit():
    allowed_types = [
        'Makeup', 'Barber Business', 'Hair Stylist', 'Lash Business', 'Nail Business'
    ]
    data = request.form
    business_name = data.get('business_name', '').strip()
    business_type = data.get('business_type', '').strip()
    description = data.get('description', '').strip()
    ui = session.get('supabase_user')

    if not ui:
        return redirect(url_for('auth_bp.login'))
    if not business_name or not business_type or not description:
        return render_template('create_business_account.html', error='All fields are required.', user=ui)
    if business_type not in allowed_types:
        return render_template('create_business_account.html', error='Invalid business type.', user=ui)
    try:
        supabase_user = supabase.table("UserAccounts").select("*").eq("auth_id", ui["auth_id"]).single().execute()

        if not supabase_user.data:
            return render_template('create_business_account.html', error='User not found')

        supabase_user_id = supabase_user.data['id']

        supabase.table('BusinessAccountRequests').insert({
            'business_name': business_name,
            'business_type': business_type,
            'description': description,
            'user_id': supabase_user_id
        }).execute()

        return render_template('create_business_account.html', success='Request submitted successfully!', user=ui)
    

    except Exception as e:
        return render_template('create_business_account.html', error=f'Error: {e}', user=ui)