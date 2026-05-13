# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install build dependencies
RUN python -m pip install --upgrade pip

# Copy project files
COPY requirements.txt .
COPY src/ src/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for the Flask app
EXPOSE 8000

# Run the Flask application with Gunicorn for production
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "src.app:app"]
