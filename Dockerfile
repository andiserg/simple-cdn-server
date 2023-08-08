FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt --default-timeout=100

COPY . ./

EXPOSE 8080
