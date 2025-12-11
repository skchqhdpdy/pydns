FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /srv/root

RUN apt update && apt install --no-install-recommends -y \
    git curl build-essential=12.12 \
    && rm -rf /var/lib/apt/lists/*

RUN apt update && \
    apt install -y default-mysql-client

COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip && \
    pip install -r ./requirements.txt

# NOTE: done last to avoid re-run of previous steps
COPY . .

ENTRYPOINT ["python3", "dns.py"]