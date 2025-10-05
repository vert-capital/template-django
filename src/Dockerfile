FROM python:3.12-trixie
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    cmake \
    libssl-dev \
    zlib1g-dev \
    libsasl2-dev \
    && git clone https://github.com/edenhill/librdkafka.git \
    && cd librdkafka \
    && git checkout v1.9.2 \
    && ./configure \
    && make \
    && make install \
    && ldconfig \
    && cd .. \
    && rm -rf librdkafka \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

ENTRYPOINT ["sh", "./docker_assets/entrypoint.sh"]

CMD ["gunicorn", "conf.asgi:application", "-b", "0.0.0.0:8080", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "warning", "-k", "uvicorn.workers.UvicornWorker"]