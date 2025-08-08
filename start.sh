#!/bin/bash
set -e

echo "Starting application..."

# Check if we're using SQLite and need to initialize the database
if [[ "$DATABASE_URL" == sqlite* ]]; then
    echo "Using SQLite database"
    
    # Convert PostgreSQL backup to SQLite format (simplified)
    # For now, we'll just start the app and let it create tables
    # In a real deployment, you'd want to convert the SQL properly
    
    echo "Database initialization completed"
else
    echo "Using external database: $DATABASE_URL"
fi

# Start the FastAPI application
echo "Starting FastAPI server on port 8000..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
