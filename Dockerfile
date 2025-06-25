# Dockerfile
FROM python:3.11-slim

# 1) Prevent writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 2) Set your working directory
WORKDIR /app

# 3) Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy your backend code
COPY backend/app.py              ./app.py
COPY backend/supabase_client.py  ./supabase_client.py
COPY backend/auth/               ./auth/
COPY backend/dashboard/          ./dashboard/

# 5) Copy your front-end templates
#    Since your Flask app does `template_folder="../frontend"`,
#    we need to put the frontend folder *beside* /app in the container
COPY frontend/                   /frontend/

# 6) Copy your .env (optional—can also be passed at runtime)
COPY .env                        ./

# 7) Expose the port your app listens on
EXPOSE 5001

# 8) Launch your Flask app exactly as you do locally
CMD ["python3", "app.py"]
