# Stage 1: Builder stage
FROM python:3.9-slim AS builder

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt to install dependencies first
COPY requirements.txt .

# Install Python dependencies (including gunicorn)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Final runtime image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy the back-end files into the container
COPY . .

# Expose the port the back-end will run on
EXPOSE 5000

# Start the back-end server with Gunicorn for production
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "app:app"]