FROM python:2.7.15-alpine

RUN apk upgrade && apk add \
    python \
    tcpdump

RUN pip install prometheus_client scapy
ENV USER=pythonuser
ENV UID=82
ENV GID=1000
RUN addgroup $USER

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "$(pwd)" \
    --ingroup "$USER" \
    --no-create-home \
    --uid "$UID" \
    "$USER"

COPY mysql-stats.py /mysql-stats.py
RUN chown pythonuser /mysql-stats.py
USER pythonuser
CMD ["python", "/mysql-stats.py"]
