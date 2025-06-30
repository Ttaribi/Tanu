from flask import render_template, session, request, jsonify
from backend.auth.auth import login_required
from . import student_profile_bp


@student_profile_bp.route('/')
@login_required
def student_profile():
  
    user = session.get('user', {})
    return render_template('student_profile.html', user=user)

@student_profile_bp.route('/update-alt-email', methods=['POST'])
@login_required
def update_alt_email():
    try:
        data = request.get_json()
        new_alt_email = data.get('alt_email', '').strip()
        
        if not new_alt_email:
            return jsonify({'success': False, 'message': 'Email cannot be empty'}), 400
        
      
        if 'user' in session:
            session['user']['alt_email'] = new_alt_email
        
        return jsonify({'success': True, 'message': 'Alternative email updated successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred'}), 500
