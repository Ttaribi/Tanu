from flask import Blueprint, jsonify, url_for, redirect, render_template, request, session
from backend.clients import supabase
from postgrest.exceptions import APIError
from functools import wraps
from . import tanuAdmin_bp
import json

# Function Description: Checks if user is an admin

def admin_account_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ui = session["supabase_user"]
        if ui["google_email"] != "ttaribi@terpmail.umd.edu":
            return redirect(url_for("auth_bp.login"))
        return f(*args, **kwargs)
    return decorated

# Function Description: Retrieves current business forms from db and sends to front end

@tanuAdmin_bp.route("/admin")
@admin_account_required
def admin_portal():
    try:
  
        response = supabase.table("BusinessAccountRequests").select("*").execute()
        data = response.data if response.data else []
      
    except Exception as e:
        data = []
    return render_template("admin_portal.html", requests=data)

# Function Description: Handles accepts a business pending on the admin page
@tanuAdmin_bp.route("/admin/approve_business_request/<int:request_id>", methods=["POST"])
@admin_account_required
def approve_business_request(request_id):

    try:
        
        response = supabase.table("BusinessAccountRequests").select("*").eq("id", request_id).execute()
        
        if not response.data:
            return jsonify({"error": "Business account request not found"}), 404
        
        request_data = response.data[0]
        
        
        update_response = supabase.table("BusinessAccountRequests").update({
            "status": "approved",
            "approved_at": "now()"
        }).eq("id", request_id).execute()
        
        return jsonify({"message": "Business account request approved successfully"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Function Description: Handles rejecting a business pending on the admin page
@tanuAdmin_bp.route("/admin/reject_business_request/<int:request_id>", methods=["POST"])
@admin_account_required
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

