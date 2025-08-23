import requests
from flask import Blueprint, redirect, request, render_template, session, url_for, jsonify
from backend.clients import supabase
from postgrest.exceptions import APIError
from . import business_public_bp
from backend.auth.auth_checks import login_required


@business_public_bp.route("<slug>")
def business_lookup():
    pass