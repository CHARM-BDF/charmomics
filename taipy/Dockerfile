FROM python:3.12

WORKDIR /app

RUN apt-get update
RUN apt-get install -y libgl1

COPY requirements.txt ./requirements.txt
COPY ./etc/taipy.env ./.env

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["python3", "src/main.py", "--host", "0.0.0.0", "--port", "5050"]
