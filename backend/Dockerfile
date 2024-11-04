# Local Development Stage
FROM python:3.11-slim-bookworm as development-stage
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app/src
ENTRYPOINT ["/bin/sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level info --reload"]
