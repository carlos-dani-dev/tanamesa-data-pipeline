#!/bin/bash

# Set PYTHONPATH to include /src
export PYTHONPATH=/src:$PYTHONPATH

# Run database ingestion
python api/db_ingestion.py

# Start the API
exec uvicorn api.app:app --host 0.0.0.0 --port 8000
