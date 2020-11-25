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

ADD requirements.txt /work/
RUN pip install --no-cache-dir -r /work/requirements.txt

WORKDIR /dev/code
