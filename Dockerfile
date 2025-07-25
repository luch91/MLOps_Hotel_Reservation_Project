# Use lightweight Python base image
FROM python:3.10-slim

# Set environment variables for cleaner logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy source code into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Expose app port
EXPOSE 5000

# Default command to run the application
CMD ["python", "application.py"]
