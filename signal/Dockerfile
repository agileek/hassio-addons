# One Dockerfile for both architectures: the HA builder passes the per-arch base image from
# build.yaml as BUILD_FROM, everything arch-specific is decided inside the build via uname -m.
#
# Two stages:
#   prepare  downloads signal-cli and puts the native libsignal library for this architecture
#            into the jar (same mechanism as before)
#   runtime  Java runtime, dbus, Python venv, and only the files the addon needs to run
#
# Build tools (curl, gnupg, zip), apt lists, pip cache and the other architecture's libsignal
# binary never reach the final image.

ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-debian:trixie

# ---------------------------------------------------------------------------- prepare
FROM $BUILD_FROM AS prepare

ARG SIGNAL_VERSION=0.14.8
ARG LIBSIGNAL_VERSION=0.102.1

# only the native libraries are needed here, not the whole root tree
COPY root/ext/libraries/libsignal-client/v${LIBSIGNAL_VERSION} /ext

RUN set -eu; \
  apt-get update; \
  apt-get install -y --no-install-recommends ca-certificates curl zip; \
  curl -fsSL "https://github.com/AsamK/signal-cli/releases/download/v${SIGNAL_VERSION}/signal-cli-${SIGNAL_VERSION}.tar.gz" | tar xz -C /; \
  mv "/signal-cli-${SIGNAL_VERSION}" /signal-cli; \
  case "$(uname -m)" in \
    aarch64) libarch=arm64 ;; \
    x86_64) libarch=x86-64 ;; \
    *) echo "unsupported architecture: $(uname -m)" >&2; exit 1 ;; \
  esac; \
  cp "/ext/${libarch}/libsignal_jni.so" /tmp/libsignal_jni.so; \
  cd /tmp; \
  zip -q -u /signal-cli/lib/libsignal-client-*.jar libsignal_jni.so

# ---------------------------------------------------------------------------- runtime
FROM $BUILD_FROM

ENV LANG=C.UTF-8

RUN set -eu; \
  apt-get update; \
  apt-get install -y --no-install-recommends ca-certificates curl gnupg; \
  curl -fsSL https://download.bell-sw.com/pki/GPG-KEY-bellsoft | gpg --dearmor -o /usr/share/keyrings/bell-sw.gpg; \
  echo "deb [signed-by=/usr/share/keyrings/bell-sw.gpg] https://apt.bell-sw.com/ stable main" > /etc/apt/sources.list.d/bellsoft.list; \
  apt-get update; \
  apt-get install -y --no-install-recommends dbus jq python3 python3-venv bellsoft-java25-runtime; \
  apt-get purge -y --auto-remove gnupg; \
  rm -rf /var/lib/apt/lists/*

COPY --from=prepare /signal-cli /signal-cli
COPY root/etc /etc
COPY root/app /app
COPY root/run.sh /run.sh

RUN set -eu; \
  python3 -m venv ~/.python_signal; \
  ~/.python_signal/bin/pip install --no-cache-dir -r /app/requirements.txt

ENTRYPOINT [ "/run.sh" ]
