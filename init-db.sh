#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
until pg_isready -h postgres -p 5432 -U postgres; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 2
done

echo "PostgreSQL is ready. Importing data..."

# Import the backup data
PGPASSWORD=postgres psql -h postgres -p 5432 -U postgres -d hungrydog < /app/hungrydog_backup.sql

echo "Data import completed successfully!"
