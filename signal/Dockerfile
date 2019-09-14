ARG BUILD_FROM=hassioaddons/base-python:2.0.3
FROM $BUILD_FROM

ENV LANG=C.UTF-8 \
    DEFAULT_JVM_OPTS="-Djava.security.egd=file:/dev/urandom" \
    JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk \
    PATH="/usr/lib/jvm/java-1.8-openjdk/bin:${PATH}"


ADD https://github.com/AsamK/signal-cli/releases/download/v0.6.2/signal-cli-0.6.2.tar.gz /signal-cli.tar.gz
ADD http://www.matthew.ath.cx/projects/java/libmatthew-java-0.8.1.tar.gz /libmatthew-java.tar.gz

RUN apk add --no-cache jq openjdk8 dbus build-base
# TODO: Merge this
RUN mkdir -p /usr/share/java/libmatthew && \
    tar xvzf /libmatthew-java.tar.gz && \
    cd /libmatthew-java-0.8.1 && \
    make unix-0.5.jar libunix-java.so && \
    install -m 644 unix-0.5.jar /usr/share/java/libmatthew && \
    install -m 755 libunix-java.so /usr/lib && \
    ln -s unix-0.5.jar /usr/share/java/libmatthew/unix.jar


#https://github.com/poppyschmo/znc-signal/blob/master/docker/Dockerfile

ADD app.py /app/
ADD requirements.txt /app/
ADD org.asamk.Signal.conf /etc/dbus-1/system.d/org.asamk.Signal.conf

RUN tar xvzf signal-cli.tar.gz && pip install -r /app/requirements.txt

COPY run.sh /

CMD [ "/run.sh" ]
