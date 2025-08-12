
# Purpose:  Initialize a single Supabase client instance that we can import
#           anywhere in Flask to talk to Supabase.

from supabase import create_client, Client
import os
import boto3
from dotenv import load_dotenv #Loads environment vars from your .env file

load_dotenv() # reads .env into python's os.environ

SUPABASE_URL = os.getenv("SUPABASE_URL") 
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
AWS_S3_ACCESS = os.getenv("AWS_S3_ACCESS")
AWS_S3_SECRET = os.getenv("AWS_S3_SECRET")
S3_BUCKET = os.getenv("S3_BUCKET")

if SUPABASE_URL is None or SUPABASE_SERVICE_ROLE_KEY is None:
    raise RuntimeError("Missing SUPABASE_URL OR ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

s3_client = boto3.client(
    "s3", 
    aws_access_key_id=AWS_S3_ACCESS, 
    aws_secret_access_key=AWS_S3_SECRET
)
    