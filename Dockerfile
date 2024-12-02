# Use official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Run collectstatic to gather static files
RUN python manage.py collectstatic --noinput

# Expose the port
EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "project_name.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
