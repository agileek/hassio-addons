ARG BUILD_FROM=homeassistant/amd64-base-debian:bookworm
FROM $BUILD_FROM

ENV SIGNAL_VERSION=0.13.0 \
    LIBSIGNAL_VERSION=0.39.2 \
    LANG=C.UTF-8

COPY root /

RUN arch="$(uname -m)"; \
        case "$arch" in \
            aarch64) cp /ext/libraries/libsignal-client/v${LIBSIGNAL_VERSION}/arm64/libsignal_jni.so /tmp/libsignal_jni.so ;; \
            armv7l) cp /ext/libraries/libsignal-client/v${LIBSIGNAL_VERSION}/armv7/libsignal_jni.so /tmp/libsignal_jni.so ;; \
            x86_64) cp /ext/libraries/libsignal-client/v${LIBSIGNAL_VERSION}/x86-64/libsignal_jni.so /tmp/libsignal_jni.so ;; \
        esac;

RUN apt update && apt install -y dbus jq python3 python3-pip zip python3-venv wget
RUN arch="$(uname -m)"; \
        case "$arch" in \
            aarch64) wget https://download.bell-sw.com/java/21.0.2+14/bellsoft-jre21.0.2+14-linux-aarch64.deb -O /tmp/java.deb ;; \
            armv7l) wget https://download.bell-sw.com/java/21.0.2+14/bellsoft-jre21.0.2+14-linux-arm32-vfp-hflt.deb -O /tmp/java.deb ;; \
            x86_64) wget https://download.bell-sw.com/java/21.0.2+14/bellsoft-jre21.0.2+14-linux-amd64.deb -O /tmp/java.deb ;; \
        esac;
RUN dpkg -i /tmp/java.deb && \
    curl -L "https://github.com/AsamK/signal-cli/releases/download/v${SIGNAL_VERSION}/signal-cli-${SIGNAL_VERSION}.tar.gz" --output "/signal-cli-${SIGNAL_VERSION}.tar.gz" && \
    tar xvzf /signal-cli-${SIGNAL_VERSION}.tar.gz -C / && \
    mv /signal-cli-${SIGNAL_VERSION} /signal-cli && \
    rm /signal-cli-${SIGNAL_VERSION}.tar.gz && \
    cd /tmp && \
    zip -u /signal-cli/lib/libsignal-client-*.jar libsignal_jni.so && \
    python3 -m venv ~/.python_signal && \
    ~/.python_signal/bin/pip install -r /app/requirements.txt

#https://github.com/poppyschmo/znc-signal/blob/master/docker/Dockerfile


ENTRYPOINT [ "/run.sh" ]
