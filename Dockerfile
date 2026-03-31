FROM python:3.13-slim

WORKDIR /app

# System dependencies for psycopg2 and pdfplumber
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5010

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl --fail http://localhost:5010/login || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5010"]
