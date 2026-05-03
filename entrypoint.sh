#!/bin/sh
# Run migrations or setup scripts
python3 seed.py

# Then start the actual web server
exec uvicorn main:app --host 0.0.0.0 --port 8000
