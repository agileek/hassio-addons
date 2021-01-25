ARG BUILD_FROM=homeassistant/amd64-base-debian:buster
FROM $BUILD_FROM

ENV SIGNAL_VERSION=0.6.11 \
    LANG=C.UTF-8

COPY root /
RUN apt update && apt install -y dbus jq python3 python3-pip default-jre && \
    curl -L "https://github.com/AsamK/signal-cli/releases/download/v${SIGNAL_VERSION}/signal-cli-${SIGNAL_VERSION}.tar.gz" --output "/signal-cli-${SIGNAL_VERSION}.tar.gz" && \
    tar xvzf /signal-cli-${SIGNAL_VERSION}.tar.gz -C / && \
    mv /signal-cli-${SIGNAL_VERSION} /signal-cli && \
    rm /signal-cli-${SIGNAL_VERSION}.tar.gz && \
    pip3 install -r /app/requirements.txt
#https://github.com/poppyschmo/znc-signal/blob/master/docker/Dockerfile


CMD [ "/run.sh" ]