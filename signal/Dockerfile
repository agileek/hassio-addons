ARG BUILD_FROM=hassioaddons/base-python:5.1.0
FROM $BUILD_FROM

ENV SIGNAL_VERSION=0.6.8 \
    LANG=C.UTF-8 \
    JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk \
    PATH="/usr/lib/jvm/java-1.8-openjdk/bin:${PATH}"

COPY root /
RUN apk add --no-cache openjdk8 dbus jq && \
    curl -L "https://github.com/AsamK/signal-cli/releases/download/v${SIGNAL_VERSION}/signal-cli-${SIGNAL_VERSION}.tar.gz" --output "/signal-cli-${SIGNAL_VERSION}.tar.gz" && \
    tar xvzf /signal-cli-${SIGNAL_VERSION}.tar.gz -C / && \
    mv /signal-cli-${SIGNAL_VERSION} /signal-cli && \
    rm /signal-cli-${SIGNAL_VERSION}.tar.gz && \
    pip install -r /app/requirements.txt
#https://github.com/poppyschmo/znc-signal/blob/master/docker/Dockerfile


CMD [ "/run.sh" ]
