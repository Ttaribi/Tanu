# Dockerfile
FROM python:3.11-slim

# 1) Prevents writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 2) Set the working directory
WORKDIR /app
ENV PYTHONPATH=/app
# 3) Installs Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Coies the backend code
COPY backend/app.py              ./app.py
COPY backend/supabase_client.py  ./supabase_client.py
COPY backend/auth/               ./auth/
COPY backend/dashboard/          ./dashboard/
COPY backend/student_profile/            ./student_profile/

# 5) This copies the front-end templates

COPY frontend/                   /frontend/

# 6) Copies the .env 
COPY .env                        ./

# 7) Exposes the port your app listens on
EXPOSE 5001

# 8) Launch the Flask app exactly as you do locally
CMD ["python3", "app.py"]
