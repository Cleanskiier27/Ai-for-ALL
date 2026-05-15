# NetworkBuster M2M Middleware - Docker Backend
# Luna.eu Cislunar Deployment

FROM python:3.11-slim

LABEL maintainer="Cleanskiier27"
LABEL description="NetworkBuster M2M Middleware - Moon 2 Mars Deep Space AI Network"

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY server.py .
COPY templates/ ./templates/

# Expose the middleware port
EXPOSE 8080

# Health check so Docker knows when the container is ready
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

CMD ["python", "server.py"]
