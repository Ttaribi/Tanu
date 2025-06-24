# ┌─────────────────────────────────────────────────────────────────────┐
# │ Dockerfile                                                        │
# └─────────────────────────────────────────────────────────────────────┘

# 1) Base off a small Python image
FROM python:3.11-slim

# 2) Prevent writing .pyc files, and make stdout/stderr unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3) Set working directory
WORKDIR /app

# 4) Copy & install only requirements first (caches nicely)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5) Copy your backend code (app.py, routes.py, supabase_client.py, etc.)
COPY backend/ ./

# 6) Copy the frontend folder into Flask’s default templates directory
#    (app.py uses template_folder="templates")
COPY frontend/ templates/

# 7) If we using a .env locally for dev creds, copy it too
#    (for production, you’d rather pass these in via -e flags to `docker run`)
COPY .env ./

# 8) Exposes the port our Flask app actually binds to
EXPOSE 5001

# 9) Launches Flask app as we do locally
CMD ["python3", "app.py"]
