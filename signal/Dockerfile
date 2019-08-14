ARG BUILD_FROM=hassioaddons/base-python:2.0.2
FROM $BUILD_FROM

ENV LANG C.UTF-8

RUN apk add --no-cache jq openjdk8-jre

# TODO 2019-08-14 Use DBUS
#https://github.com/poppyschmo/znc-signal/blob/master/docker/Dockerfile
ADD https://github.com/AsamK/signal-cli/releases/download/v0.6.2/signal-cli-0.6.2.tar.gz /signal-cli.tar.gz
ADD app.py /app/
ADD requirements.txt /app/

RUN tar xvzf signal-cli.tar.gz && pip install -r /app/requirements.txt

COPY run.sh /

CMD [ "/run.sh" ]
