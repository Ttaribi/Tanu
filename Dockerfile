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
RUN pip install --no-cache-dir --upgrade pip \
&& pip install --no-cache-dir -r requirements.txt

# 4) Copying immutable folders into container
# Not needed for dev, but good for prod
#COPY backend/ ./backend/
#COPY frontend/ ./frontend/

# 7) Exposes the port your app listens on
EXPOSE 5001

# 8) Launch the Flask app 
CMD ["python3", "backend/app.py"]
