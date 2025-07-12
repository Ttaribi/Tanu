from flask import redirect, url_for, render_template, session, request, jsonify
from supabase_client import supabase
from backend.auth.auth import login_required
from . import student_profile_bp


@student_profile_bp.route('/')
@login_required
def student_profile():
    
    # Get user session info
    ui = session.get("supabase_user")
    if not ui:
        return redirect(url_for("auth_bp.login"))

    # Fetch the latest full profile from Supabase
    try:
        profile = (
            supabase
            .table("UserAccounts")
            .select("*")
            .eq("auth_id", ui["id"])
            .single()
            .execute()
            .data
        )

        # Save updated profile to session
        session["supabase_user"] = profile

        # Pass it to the HTML
        return render_template("student_profile.html", user=profile)

    except Exception as e:
        return f"Error fetching profile: {e}", 500

@student_profile_bp.route('/update-alt-email', methods=['POST'])
@login_required
def update_alt_email():
    try:
        data = request.get_json()
        new_alt_email = data.get('alt_email', '').strip()

        ui = session.get("supabase_user")

        supabase.table("UserAccounts").select('*').eq("auth_id", ui["id"]).upsert({"alt_email": new_alt_email}, on_conflict=["auth_id"]).execute()
        
        if not new_alt_email:
            return jsonify({'success': False, 'message': 'Email cannot be empty'}), 400
        
      
        if 'user' in session:
            session['user']['alt_email'] = new_alt_email
        
        return jsonify({'success': True, 'message': 'Alternative email updated successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred'}), 500
