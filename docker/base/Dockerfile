# syntax=docker/dockerfile:1
FROM arm32v7/ubuntu:22.04

# Remove interactivity from apt commands
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update --fix-missing

# Installing linux utilities
RUN apt install build-essential -y
RUN apt install g++ -y
RUN apt install sudo -y
RUN apt install systemctl -y
RUN apt install lsb-release -y
RUN apt install gcc -y

# Installing python3.10
RUN apt install python3.10-venv -y
RUN apt install python3.10-dev -y
RUN ln -s /usr/bin/python3 /usr/bin/python

# Installing utilities
RUN apt install postgresql postgresql-contrib -y
COPY docker/base/pg_hba.conf /etc/postgresql/14/main/pg_hba.conf
RUN apt install libpq-dev -y
RUN service postgresql restart

# Define timezone
RUN apt install tzdata -y
RUN ln -sf /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone

# Cleaning cache to reduce image size
RUN apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installing all python requirements
COPY requirements.txt /app/
RUN python -m venv .env && \
    . .env/bin/activate && \
    pip install -r requirements.txt
