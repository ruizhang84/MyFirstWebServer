# --- Stage 1: Build React frontend ---
FROM node:20 as frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# --- Stage 2: Build backend and serve everything with NGINX ---
FROM python:3.10-slim as production

# Install system packages for pdf2image
RUN apt-get update && \
    apt-get install -y poppler-utils nginx && \
    rm -rf /var/lib/apt/lists/*

# Set working dir for backend
WORKDIR /app

# Copy backend and install Python deps
COPY backend/ ./backend/
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Copy frontend build to NGINX html folder
COPY --from=frontend-builder /app/frontend/build /var/www/html

# Copy custom NGINX config
COPY nginx.conf /etc/nginx/sites-available/default

# Expose ports
EXPOSE 80

# Copy and run an entrypoint to run both Gunicorn and NGINX
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
