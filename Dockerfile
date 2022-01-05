FROM python:3.10.1-slim-buster
RUN apt-get update && apt-get install -y git gcc libssl-dev musl-dev libmariadb-dev
WORKDIR /app
ADD requirements.txt /app/
RUN pip install --upgrade pip pyopenssl
RUN pip install -r requirements.txt
COPY . /app
