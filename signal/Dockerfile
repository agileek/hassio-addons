ARG BUILD_FROM=homeassistant/amd64-base-debian:buster
FROM $BUILD_FROM AS builder

WORKDIR /workspace
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN curl -L https://github.com/signalapp/zkgroup/archive/v0.7.1.tar.gz --output /workspace/zkgroup.tar.gz &&\
    tar xvzf /workspace/zkgroup.tar.gz && \
    rm /workspace/zkgroup.tar.gz
RUN apt update && apt install make build-essential -y
RUN cd /workspace/zkgroup-0.7.1 && make libzkgroup


ARG BUILD_FROM=homeassistant/amd64-base-debian:buster
FROM $BUILD_FROM

ENV SIGNAL_VERSION=0.7.4 \
    LANG=C.UTF-8

COPY root /
RUN apt update && apt install -y dbus jq python3 python3-pip default-jre zip && \
    curl -L "https://github.com/AsamK/signal-cli/releases/download/v${SIGNAL_VERSION}/signal-cli-${SIGNAL_VERSION}.tar.gz" --output "/signal-cli-${SIGNAL_VERSION}.tar.gz" && \
    tar xvzf /signal-cli-${SIGNAL_VERSION}.tar.gz -C / && \
    mv /signal-cli-${SIGNAL_VERSION} /signal-cli && \
    rm /signal-cli-${SIGNAL_VERSION}.tar.gz && \
    zip -d /signal-cli/lib/zkgroup-java-*.jar libzkgroup.so && \
    pip3 install -r /app/requirements.txt

COPY --from=builder /workspace/zkgroup-0.7.1/target/release/libzkgroup.so /signal-cli/lib/libzkgroup.so
#https://github.com/poppyschmo/znc-signal/blob/master/docker/Dockerfile


CMD [ "/run.sh" ]