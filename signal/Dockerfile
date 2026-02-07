ARG BUILD_FROM=amd64-base-debian:trixie
FROM $BUILD_FROM

ENV SIGNAL_VERSION=0.13.24 \
  LIBSIGNAL_VERSION=0.87.0 \
  LANG=C.UTF-8

COPY root /

RUN arch="$(uname -m)"; \
  case "$arch" in \
  aarch64) cp /ext/libraries/libsignal-client/v${LIBSIGNAL_VERSION}/arm64/libsignal_jni.so /tmp/libsignal_jni.so ;; \
  armv7l) cp /ext/libraries/libsignal-client/v${LIBSIGNAL_VERSION}/armv7/libsignal_jni.so /tmp/libsignal_jni.so ;; \
  x86_64) cp /ext/libraries/libsignal-client/v${LIBSIGNAL_VERSION}/x86-64/libsignal_jni.so /tmp/libsignal_jni.so ;; \
  esac;

RUN apt update && apt install -y gnupg
RUN curl -L https://download.bell-sw.com/pki/GPG-KEY-bellsoft | apt-key add -
RUN echo "deb https://apt.bell-sw.com/ stable main" | tee /etc/apt/sources.list.d/bellsoft.list

RUN apt update && apt install -y dbus jq python3 python3-pip zip bellsoft-java21-runtime python3-venv && \
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
