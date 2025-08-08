# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY tests/ ./tests/
COPY main.py .
COPY Mobile_Food_Facility_Permit_2.csv .
COPY hungrydog_backup.sql .
COPY init-db.sh .
COPY start.sh .

# Note: .env files are not needed in Cloud Run (using environment variables instead)

# Make scripts executable
RUN chmod +x init-db.sh start.sh

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["./start.sh"]
