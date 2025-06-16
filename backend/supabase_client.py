# ─────────────────────────────────────────────────────────────────────────────
# backend/supabase_client.py
#
# Purpose:  Initialize a single Supabase client instance that we can import
#           anywhere in Flask to talk to Supabase.
# ─────────────────────────────────────────────────────────────────────────────

from supabase import create_client, Client
import os
from dotenv import load_dotenv #Loads environment vars from your .env file

load_dotenv() # reads .env into python's os.environ

SUPABASE_URL = os.getenv("SUPABASE_URL") #Gets var set in .env
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

#Checks if vars are there or not
if SUPABASE_URL is None or SUPABASE_KEY is None:
    raise RuntimeError("Missing SUPABASE_URL OR SUPABASE_KEY")

# CREATES THE CLIENT
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)