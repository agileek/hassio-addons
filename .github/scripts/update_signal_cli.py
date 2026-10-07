#!/usr/bin/env python3
"""Compares the signal-cli version pinned in signal/Dockerfile with the latest GitHub release, resolves the
libsignal-client version that release is built against, downloads the prebuilt libsignal_jni.so for
x86-64 and arm64, and rewrites Dockerfile, build-libsignal.yml, CHANGELOG.md and the binaries folder.
Writes `updated`, versions to $GITHUB_OUTPUT. Exits 0 without changes when nothing is to do or when the
prebuilt binaries are not published yet (that case is logged as a notice and retried by the schedule).

Only the standard library is used, so the workflow needs no pip install.
"""
import io
import json
import os
import pathlib
import re
import sys
import tarfile
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCKERFILE = ROOT / "signal" / "Dockerfile"
WORKFLOW = ROOT / ".github" / "workflows" / "build-libsignal.yml"
CHANGELOG = ROOT / "signal" / "CHANGELOG.md"
BINDIR = ROOT / "signal" / "root" / "ext" / "libraries" / "libsignal-client"
ARCHES = {"x86-64": "x86_64-unknown-linux-gnu", "arm64": "aarch64-unknown-linux-gnu"}


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": "hassio-addons-update", "Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token and "api.github.com" in url:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode()


def output(**kv):
    path = os.environ.get("GITHUB_OUTPUT")
    lines = [f"{k}={v}" for k, v in kv.items()]
    if path:
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


def notice(msg):
    print(f"::notice::{msg}")


def main():
    dockerfile = DOCKERFILE.read_text(encoding="utf-8")
    m_sig = re.search(r"SIGNAL_VERSION=(\S+)", dockerfile)
    m_lib = re.search(r"LIBSIGNAL_VERSION=(\S+)", dockerfile)
    old_signal, old_lib = m_sig.group(1).rstrip("\\").strip(), m_lib.group(1).rstrip("\\").strip()

    latest = json.loads(get("https://api.github.com/repos/AsamK/signal-cli/releases/latest"))["tag_name"].lstrip("v")
    if latest == old_signal:
        notice(f"signal-cli {old_signal} is current")
        output(updated="false")
        return

    # signal-cli -> signal-service version -> libsignal-client version (both are gradle version catalogs)
    cat = get(f"https://raw.githubusercontent.com/AsamK/signal-cli/v{latest}/gradle/libs.versions.toml")
    service = re.search(r'^signal-service\s*=\s*"([^"]+)"', cat, re.M).group(1)
    cat2 = None
    for ref in (f"v{service}", service):  # the tag carries a v prefix, the version string does not
        try:
            cat2 = get(f"https://raw.githubusercontent.com/Turasa/libsignal-service-java/{ref}/gradle/libs.versions.toml")
            break
        except Exception:  # noqa: BLE001
            continue
    if cat2 is None:
        raise SystemExit(f"could not fetch the libsignal-service-java catalog for {service}")
    lib = re.search(r'^libsignal-client\s*=\s*"([^"]+)"', cat2, re.M).group(1)
    print(f"signal-cli {old_signal} -> {latest}, signal-service {service}, libsignal-client {old_lib} -> {lib}")

    # prebuilt binaries: all or nothing, otherwise wait for the next run
    blobs = {}
    for folder, triple in ARCHES.items():
        url = f"https://github.com/exquo/signal-libs-build/releases/download/libsignal_v{lib}/libsignal_jni.so-v{lib}-{triple}.tar.gz"
        try:
            blobs[folder] = get(url, binary=True)
        except Exception as e:  # noqa: BLE001
            notice(f"prebuilt libsignal {lib} for {folder} not available yet ({e}); trying again next run")
            output(updated="false")
            return

    for old in BINDIR.glob("v*"):
        for f in old.rglob("*"):
            if f.is_file():
                f.unlink()
        for d in sorted(old.rglob("*"), reverse=True):
            d.rmdir()
        old.rmdir()
    for folder, blob in blobs.items():
        dest = BINDIR / f"v{lib}" / folder
        dest.mkdir(parents=True)
        with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tar:
            member = next(m for m in tar.getmembers() if m.name.endswith("libsignal_jni.so"))
            (dest / "libsignal_jni.so").write_bytes(tar.extractfile(member).read())

    DOCKERFILE.write_text(dockerfile.replace(f"SIGNAL_VERSION={old_signal}", f"SIGNAL_VERSION={latest}").replace(f"LIBSIGNAL_VERSION={old_lib}", f"LIBSIGNAL_VERSION={lib}"), encoding="utf-8")
    wf = WORKFLOW.read_text(encoding="utf-8")
    WORKFLOW.write_text(re.sub(r"LIBSIGNAL_VERSION: '[^']+'", f"LIBSIGNAL_VERSION: '{lib}'", wf), encoding="utf-8")

    entry = f"- Update signal-cli to {latest} (libsignal-client {lib})\n"
    log = CHANGELOG.read_text(encoding="utf-8")
    if "## Unreleased" in log:
        log = log.replace("## Unreleased\n", "## Unreleased\n" + entry, 1)
    else:
        log = log.replace("# Changelog\n\n", "# Changelog\n\n## Unreleased\n" + entry + "\n", 1)
    CHANGELOG.write_text(log, encoding="utf-8")

    output(updated="true", signal_version=latest, old_signal_version=old_signal, libsignal_version=lib, old_libsignal_version=old_lib)


if __name__ == "__main__":
    sys.exit(main())
