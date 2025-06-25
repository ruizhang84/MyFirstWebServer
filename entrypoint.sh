#!/bin/bash

# Start Gunicorn (Flask backend)
gunicorn -w 4 -b 127.0.0.1:5000 backend.app:app &

# Start NGINX in foreground
nginx -g "daemon off;"
