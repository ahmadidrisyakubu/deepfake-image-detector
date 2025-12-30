# Use slim Python image to reduce base size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p uploads static templates

# Expose port
EXPOSE 5000

# Copy and set permissions for the start script
COPY start.sh .
RUN chmod +x start.sh

# Run the application using the start script
CMD ["./start.sh"]
