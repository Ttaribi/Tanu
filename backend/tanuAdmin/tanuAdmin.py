from flask import Blueprint, jsonify, url_for, redirect, render_template, request, session
from backend.clients import supabase
from postgrest.exceptions import APIError
from functools import wraps
from . import tanuAdmin_bp
from backend.auth.auth_checks import role_required
import json


# Function Description: Retrieves current business forms from db and sends to front end

@tanuAdmin_bp.route("/admin")
@role_required('admin')
def admin_portal():
    try:
  
        response = supabase.table("BusinessAccountRequests").select("*").eq("status", "0").execute()
        data = response.data if response.data else []
      
    except Exception as e:
        data = []
    return render_template("admin_portal.html", requests=data)

# Function Description: Handles accepts a business pending on the admin page
@tanuAdmin_bp.route("/admin/approve_business_request/<int:request_id>", methods=["POST"])
@role_required('admin')
def approve_business_request(request_id):

    try:
        
        response = supabase.table("BusinessAccountRequests").select("*").eq("id", request_id).execute()
        
        if not response.data:
            return jsonify({"error": "Business account request not found"}), 404
        
        request_data = response.data[0]
        
        
        update_response = supabase.table("BusinessAccountRequests").update({
            "status": "1",
            "approved_at": "now()"
        }).eq("id", request_id).execute()

        
        
        return redirect(url_for('tanuAdmin_bp.admin_portal'))
        
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Function Description: Handles rejecting a business pending on the admin page
@tanuAdmin_bp.route("/admin/reject_business_request/<int:request_id>", methods=["POST"])
@role_required('admin')
def reject_business_request(request_id):

    try:
       
        response = supabase.table("BusinessAccountRequests").select("*").eq("id", request_id).single().execute()
        
        if not response.data:
            return jsonify({"error": "Business account request not found"}), 404
        
        request_data = response.data
        
        
        supabase.table("RejectedBusinessAccounts").insert({
            "user_id": request_data["user_id"],
            "business_name": request_data["business_name"],
            "business_type": request_data["business_type"],
            "description": request_data["description"]
        }).execute()

        supabase.table("BusinessAccountRequests").delete().eq("id", request_id).execute()
        
        return redirect(url_for('tanuAdmin_bp.admin_portal'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# refresh user profile for testing reasons
@tanuAdmin_bp.route("/refresh")
@role_required('student')
def refresh():
    profile = (
        supabase
        .table('UserAccounts')
        .select("*")
        .eq("auth_id", session['supabase_user']['auth_id'])
        .single()
        .execute()
        .data
    )
    session['supabase_user'] = profile
    return "refreshed"