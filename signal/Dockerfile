ARG BUILD_FROM=hassioaddons/base-python:5.1.0
FROM $BUILD_FROM

ENV SIGNAL_VERSION=0.6.7 \
    LANG=C.UTF-8 \
    JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk \
    PATH="/usr/lib/jvm/java-1.8-openjdk/bin:${PATH}"

COPY root /
# Libmatthew is for dbus
RUN curl http://www.matthew.ath.cx/projects/java/libmatthew-java-0.8.1.tar.gz --output /libmatthew-java.tar.gz && \
    apk add --no-cache jq openjdk8 dbus build-base && \
    mkdir -p /usr/share/java/libmatthew && \
    tar xvzf /libmatthew-java.tar.gz && \
    cd /libmatthew-java-0.8.1 && \
    make unix-0.5.jar libunix-java.so && \
    install -m 644 unix-0.5.jar /usr/share/java/libmatthew && \
    install -m 755 libunix-java.so /usr/lib && \
    ln -s unix-0.5.jar /usr/share/java/libmatthew/unix.jar && \
    rm /libmatthew-java.tar.gz && \
    curl -L "https://github.com/AsamK/signal-cli/releases/download/v${SIGNAL_VERSION}/signal-cli-${SIGNAL_VERSION}.tar.gz" --output "/signal-cli-${SIGNAL_VERSION}.tar.gz" && \
    tar xvzf /signal-cli-${SIGNAL_VERSION}.tar.gz -C / && \
    mv /signal-cli-${SIGNAL_VERSION} /signal-cli && \
    rm /signal-cli-${SIGNAL_VERSION}.tar.gz && \
    pip install -r /app/requirements.txt
#https://github.com/poppyschmo/znc-signal/blob/master/docker/Dockerfile


CMD [ "/run.sh" ]
