ARG BUILD_FROM=homeassistant/amd64-base-debian:buster
FROM $BUILD_FROM

ENV SIGNAL_VERSION=0.7.4 \
    ZKGROUP_VERSION=0.7.0 \
    LANG=C.UTF-8

COPY root /

RUN arch="$(uname -m)"; \
        case "$arch" in \
            aarch64) cp /ext/libraries/zkgroup/v${ZKGROUP_VERSION}/arm64/libzkgroup.so /tmp/libzkgroup.so ;; \
			armv7l) cp /ext/libraries/zkgroup/v${ZKGROUP_VERSION}/armv7/libzkgroup.so /tmp/libzkgroup.so ;; \
            x86_64) cp /ext/libraries/zkgroup/v${ZKGROUP_VERSION}/x86-64/libzkgroup.so /tmp/libzkgroup.so ;; \
        esac;

RUN apt update && apt install -y dbus jq python3 python3-pip default-jre zip && \
    curl -L "https://github.com/AsamK/signal-cli/releases/download/v${SIGNAL_VERSION}/signal-cli-${SIGNAL_VERSION}.tar.gz" --output "/signal-cli-${SIGNAL_VERSION}.tar.gz" && \
    tar xvzf /signal-cli-${SIGNAL_VERSION}.tar.gz -C / && \
    mv /signal-cli-${SIGNAL_VERSION} /signal-cli && \
    rm /signal-cli-${SIGNAL_VERSION}.tar.gz && \
    cd /tmp && \
    zip -u /signal-cli/lib/zkgroup-java-*.jar libzkgroup.so && \
    cd - && \
    pip3 install -r /app/requirements.txt

#https://github.com/poppyschmo/znc-signal/blob/master/docker/Dockerfile


CMD [ "/run.sh" ]