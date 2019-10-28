ARG BUILD_FROM=hassioaddons/base-python:2.1.0
FROM $BUILD_FROM

ENV LANG=C.UTF-8 \
    JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk \
    PATH="/usr/lib/jvm/java-1.8-openjdk/bin:${PATH}"


ADD https://github.com/AsamK/signal-cli/releases/download/v0.6.3/signal-cli-0.6.3.tar.gz /signal-cli.tar.gz
ADD http://www.matthew.ath.cx/projects/java/libmatthew-java-0.8.1.tar.gz /libmatthew-java.tar.gz

RUN apk add --no-cache jq openjdk8 dbus build-base && \
    mkdir -p /usr/share/java/libmatthew && \
    tar xvzf /libmatthew-java.tar.gz && \
    cd /libmatthew-java-0.8.1 && \
    make unix-0.5.jar libunix-java.so && \
    install -m 644 unix-0.5.jar /usr/share/java/libmatthew && \
    install -m 755 libunix-java.so /usr/lib && \
    ln -s unix-0.5.jar /usr/share/java/libmatthew/unix.jar

#https://github.com/poppyschmo/znc-signal/blob/master/docker/Dockerfile

COPY root /

RUN tar xvzf signal-cli.tar.gz && pip install -r /app/requirements.txt

CMD [ "/run.sh" ]
