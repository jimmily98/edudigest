# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies (including FFmpeg)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure the data directories exist
RUN mkdir -p data/uploads data/transcripts

# Expose the port the app runs on (Render uses PORT env var)
EXPOSE 10000

# Run the application using gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT src.backend.app:app
