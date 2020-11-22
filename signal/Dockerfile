ARG BUILD_FROM=homeassistant/armv7-base-debian:buster
FROM $BUILD_FROM

ENV SIGNAL_VERSION=0.6.11 \
    LANG=C.UTF-8 \
    JAVA_HOME=/jre \
    PATH="/jre/bin:${PATH}"

COPY root /
RUN apt update && apt install -y dbus jq python3 python3-pip && \
    curl -L "https://github.com/AsamK/signal-cli/releases/download/v${SIGNAL_VERSION}/signal-cli-${SIGNAL_VERSION}.tar.gz" --output "/signal-cli-${SIGNAL_VERSION}.tar.gz" && \
    tar xvzf /signal-cli-${SIGNAL_VERSION}.tar.gz -C / && \
    mv /signal-cli-${SIGNAL_VERSION} /signal-cli && \
    rm /signal-cli-${SIGNAL_VERSION}.tar.gz && \
    curl -L "https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.9.1%2B1/OpenJDK11U-jre_arm_linux_hotspot_11.0.9.1_1.tar.gz" --output "/jre11.tar.gz" && \
    tar xvzf /jre11.tar.gz -C / && \
    mv /jdk-11.0.9.1+1-jre /jre && \
    rm /jre11.tar.gz && \
    pip install -r /app/requirements.txt
#https://github.com/poppyschmo/znc-signal/blob/master/docker/Dockerfile


CMD [ "/run.sh" ]
