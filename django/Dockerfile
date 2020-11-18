FROM python:3.8
ENV PYTHONUNBUFFERED 1

ADD ./.bashrc /root

RUN apt-get update && \
    apt-get install -y \
    git \
    zip \
    unzip \
    vim \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/html

ADD requirements.txt /var/www/html/
RUN pip install --no-cache-dir -r requirements.txt
