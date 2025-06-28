# Use an official Python runtime as a parent image
FROM python:3.11.2-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies that might be needed by psycopg2 or other libraries
# Add these if you encounter issues during pip install, e.g., for psycopg2-binary:
# RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# It's good practice to install Gunicorn here if it's your WSGI server
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend application code into the container at /app
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application using Gunicorn
# This assumes your Flask app instance is named 'app' in 'backend/app.py'
# The working directory is /app, which contains the 'backend' subdirectory.
# So, the module path is 'backend.app:app'.
# Ensure that when this container runs, it can connect to your PostgreSQL database.
# Database initialization (flask init-db) should be handled as a separate step
# during deployment, not typically within this Docker CMD.
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "backend.app:app"]
