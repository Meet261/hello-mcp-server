FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only what's needed
COPY app/ ./app
COPY templates/ ./templates
COPY static/ ./static

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
