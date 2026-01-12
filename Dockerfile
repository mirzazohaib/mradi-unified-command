# ==========================================
# 1. BASE IMAGE (Secure & Lightweight)
# ==========================================
# We use Python 3.12 Slim on Debian Bookworm.
# 'Slim' reduces attack surface area by removing unnecessary tools.
FROM python:3.12-slim-bookworm

# ==========================================
# 2. ENVIRONMENT CONFIG
# ==========================================
# PYTHONUNBUFFERED: Ensures logs stream immediately to the dashboard (Critical for Telemetry)
# PYTHONDONTWRITEBYTECODE: Prevents .pyc files from cluttering the container
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory inside the container
WORKDIR /app

# ==========================================
# 3. SYSTEM DEPENDENCIES (Resilience)
# ==========================================
# We install 'curl' to enable Health Checks (e.g., HEALTHCHECK CMD curl --fail ...)
# apt-get clean reduces image size.
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# ==========================================
# 4. PYTHON DEPENDENCIES (Layer Caching)
# ==========================================
# COPY requirements first! Docker caches this layer.
# If you change code but not requirements, Docker skips this slow step.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ==========================================
# 5. APPLICATION CODE
# ==========================================
COPY . .

# ==========================================
# 6. SECURITY HARDENING (Governance)
# ==========================================
# CRITICAL: Create a non-root user. 
# Running as root inside a container is a security risk.
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app

# Switch to the secure user
USER appuser

# ==========================================
# 7. RUNTIME CONFIGURATION
# ==========================================
# Document that this container listens on port 8000
EXPOSE 8000

# Start the application server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]