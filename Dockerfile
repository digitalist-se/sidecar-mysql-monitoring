FROM python:2.7.15-alpine

RUN apk upgrade && apk add \
    python \
    tcpdump

RUN pip install prometheus_client scapy

COPY mysql-stats.py /mysql-stats.py
CMD ["python", "/mysql-stats.py"]
