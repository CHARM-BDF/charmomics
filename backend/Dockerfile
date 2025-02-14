# Local Development Stage
FROM python:3.11-slim-bookworm AS development-stage
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN apt-get update
RUN apt-get install -y samtools=1.16.1-1 tabix=1.16+ds-3
COPY ./src /app/src
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info", "--reload"]
