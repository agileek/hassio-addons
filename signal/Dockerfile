# One Dockerfile for both architectures: the HA builder passes the per-arch base image from
# build.yaml as BUILD_FROM, everything arch-specific is decided inside the build via uname -m.
#
# Two stages:
#   prepare  downloads signal-cli and leaves exactly one native libsignal library in the jar:
#            the bundled one on amd64, the vendored one on aarch64
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
  jar="$(ls /signal-cli/lib/libsignal-client-*.jar)"; \
  # libsignal loads the bundled library named libsignal_jni_<os.arch>.so first, then libsignal_jni.so. \
  # The jar ships libsignal_jni_amd64.so plus macOS .dylib and Windows .dll files; keep exactly one library per image. \
  case "$(uname -m)" in \
    aarch64) \
      cp /ext/arm64/libsignal_jni.so /tmp/libsignal_jni_aarch64.so; \
      (cd /tmp && zip -q -u "$jar" libsignal_jni_aarch64.so); \
      zip -q -d "$jar" libsignal_jni_amd64.so ;; \
    x86_64) ;; \
    *) echo "unsupported architecture: $(uname -m)" >&2; exit 1 ;; \
  esac; \
  # one call: fails only if neither pattern matches, so a jar without .dll still builds \
  zip -q -d "$jar" "*.dylib" "*.dll"

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
