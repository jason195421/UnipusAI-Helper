#!/usr/bin/env python3
"""Download the platform's bundled FFmpeg/ffprobe into ffmpeg/<platform-id>/.

The binaries come from the @ffmpeg-installer / @ffprobe-installer npm packages,
which ship standalone, statically linked executables.  Both the npmmirror
mirror (reachable from mainland China) and the public npm registry (used by
GitHub Actions macOS runners) serve the same tarballs.

Usage:
    python scripts/fetch_ffmpeg.py
    python scripts/fetch_ffmpeg.py --registry https://registry.npmjs.org
    python scripts/fetch_ffmpeg.py --platform darwin-arm64
"""
from __future__ import annotations

import argparse
import io
import os
import sys
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from unipus_helper.ffmpeg_runtime import platform_id  # noqa: E402

DEFAULT_REGISTRY = "https://registry.npmmirror.com"

# package name -> version, per platform id
PACKAGES = {
    "win32-x64":     (("@ffmpeg-installer/win32-x64", "4.1.0"),
                      ("@ffprobe-installer/win32-x64", "5.1.0")),
    "darwin-arm64":  (("@ffmpeg-installer/darwin-arm64", "4.1.5"),
                      ("@ffprobe-installer/darwin-arm64", "5.0.1")),
    "darwin-x64":    (("@ffmpeg-installer/darwin-x64", "4.1.0"),
                      ("@ffprobe-installer/darwin-x64", "5.1.0")),
    "linux-x64":     (("@ffmpeg-installer/linux-x64", "4.1.0"),
                      ("@ffprobe-installer/linux-x64", "5.2.0")),
    "linux-arm64":   (("@ffmpeg-installer/linux-arm64", "4.1.4"),
                      ("@ffprobe-installer/linux-arm64", "5.0.1")),
}
def _exe_suffix(pid: str) -> str:
    """Binary extension for the *target* platform, not the host running this."""
    return ".exe" if pid.startswith("win") else ""


def tarball_url(registry: str, name: str, version: str) -> str:
    scope, _, pkg = name.partition("/")
    short = pkg or scope
    return registry.rstrip("/") + "/" + name + "/-/" + short + "-" + version + ".tgz"


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "UnipusAI-Helper/fetch-ffmpeg"})
    with urllib.request.urlopen(request, timeout=180) as response:
        return response.read()


def extract_binary(blob: bytes, member_name: str, destination: Path) -> None:
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as archive:
        member = next(
            (m for m in archive.getmembers()
             if m.name.endswith("/" + member_name) or m.name == member_name),
            None,
        )
        if member is None:
            raise RuntimeError(member_name + " not found in tarball")
        source = archive.extractfile(member)
        if source is None:
            raise RuntimeError("cannot read " + member.name)
        destination.write_bytes(source.read())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", default=DEFAULT_REGISTRY)
    parser.add_argument("--platform", default=None,
                        help="override auto-detected platform id")
    parser.add_argument("--force", action="store_true",
                        help="re-download even if the binaries already exist")
    args = parser.parse_args()

    pid = args.platform or platform_id()
    if pid not in PACKAGES:
        print("Unsupported platform id: " + pid, file=sys.stderr)
        return 1

    exe = _exe_suffix(pid)
    target = ROOT / "ffmpeg" / pid
    target.mkdir(parents=True, exist_ok=True)
    ffmpeg = target / ("ffmpeg" + exe)
    ffprobe = target / ("ffprobe" + exe)

    if not args.force and ffmpeg.is_file() and ffprobe.is_file():
        print("Already present: " + str(target))
        return 0

    binaries = (("ffmpeg" + exe, ffmpeg), ("ffprobe" + exe, ffprobe))
    for (name, version), (member, binary) in zip(PACKAGES[pid], binaries):
        url = tarball_url(args.registry, name, version)
        print("Downloading " + name + "@" + version + " -> " + binary.name)
        blob = download(url)
        extract_binary(blob, member, binary)
        if exe == "":
            os.chmod(binary, 0o755)
        print("  " + format(binary.stat().st_size, ",") + " bytes")

    print("Bundled FFmpeg ready at " + str(target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
