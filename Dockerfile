# app/Dockerfile

FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# RUN pip3 install -r requirements.txt
RUN pip3 install -e .

EXPOSE 8501


