# 1. Base Image: Use 3.12 Slim on Debian Bookworm (Stable & Fast)
FROM python:3.12-slim-bookworm

# 2. Set environment variables to prevent Python from buffering stdout/stderr
#    (This ensures your logs show up in the console immediately)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 3. Set the working directory
WORKDIR /app

# 4. Install system dependencies (Optional but good for 'Airbus-Ready' robustness)
#    We install curl for healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy dependencies first
COPY requirements.txt .

# 6. Install Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy the rest of the code
COPY . .

# 8. Create a non-root user for security (Airbus-Ready Requirement!)
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# 9. Expose the port
EXPOSE 8000

# 10. Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]