# Local Development Stage
FROM python:3.11-slim-bookworm AS development-stage
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app/src
RUN apt-get update && apt-get install -y --no-install-recommends samtools=1.16.1-1 tabix=1.16+ds-3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info", "--reload"]

# Production Build Stage
FROM python:3.11-slim-bookworm AS production-stage
WORKDIR /app
COPY logging.conf /app/logging.conf
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app/src
RUN apt-get update && apt-get install -y --no-install-recommends samtools=1.16.1-1 tabix=1.16+ds-3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info", "--reload"]