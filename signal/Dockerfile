ARG BUILD_FROM=homeassistant/amd64-base-debian:bullseye
FROM $BUILD_FROM

ENV SIGNAL_VERSION=0.10.8 \
    LIBSIGNAL_VERSION=0.17.0 \
    LANG=C.UTF-8

COPY root /

RUN arch="$(uname -m)"; \
        case "$arch" in \
            aarch64) cp /ext/libraries/libsignal-client/v${LIBSIGNAL_VERSION}/arm64/libsignal_jni.so /tmp/libsignal_jni.so ;; \
			armv7l) cp /ext/libraries/libsignal-client/v${LIBSIGNAL_VERSION}/armv7/libsignal_jni.so /tmp/libsignal_jni.so ;; \
            x86_64) cp /ext/libraries/libsignal-client/v${LIBSIGNAL_VERSION}/x86-64/libsignal_jni.so /tmp/libsignal_jni.so ;; \
        esac;

RUN apt update && apt install -y dbus jq python3 python3-pip openjdk-17-jre zip && \
    curl -L "https://github.com/AsamK/signal-cli/releases/download/v${SIGNAL_VERSION}/signal-cli-${SIGNAL_VERSION}-Linux.tar.gz" --output "/signal-cli-${SIGNAL_VERSION}.tar.gz" && \
    tar xvzf /signal-cli-${SIGNAL_VERSION}.tar.gz -C / && \
    mv /signal-cli-${SIGNAL_VERSION} /signal-cli && \
    rm /signal-cli-${SIGNAL_VERSION}.tar.gz && \
    cd /tmp && \
    zip -u /signal-cli/lib/libsignal-client-*.jar libsignal_jni.so && \
    cd - && \
    pip3 install -r /app/requirements.txt

#https://github.com/poppyschmo/znc-signal/blob/master/docker/Dockerfile


ENTRYPOINT [ "/run.sh" ]
