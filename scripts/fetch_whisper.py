#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download the Whisper model checkpoint into whisper_models/.

The checkpoint is bundled into the installer (see UnipusAI-Helper.spec) and
handed to whisper.load_model(name, download_root=<this dir>) at runtime.
whisper's own _download() verifies the file's SHA256 against the checksum
embedded in the official URL and reuses it without any network access, so a
fresh install never has to fetch ~145 MB from the internet.

The script first reuses any already-downloaded official checkpoint (the user's
~/.cache/whisper cache, XDG_CACHE_HOME, or --source) and only falls back to
downloading from the official Azure endpoints when no verified copy exists.

Usage:
    python scripts/fetch_whisper.py
    python scripts/fetch_whisper.py --force
    python scripts/fetch_whisper.py --source D:/models/base.pt
    python scripts/fetch_whisper.py --registry https://openaipublic.blob.core.windows.net
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = "https://openaipublic.azureedge.net"

# name -> (sha256 embedded in the official URL, filename).  Keep the checksum
# identical to whisper._MODELS so load_model() trusts the bundled file.
MODELS = {
    "base": (
        "ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e",
        "base.pt",
    ),
}

# Official mirrors that serve the very same bytes.
MIRRORS = (
    "https://openaipublic.azureedge.net",
    "https://openaipublic.blob.core.windows.net",
)


def model_url(registry: str, name: str, sha: str) -> str:
    return registry.rstrip("/") + "/main/whisper/models/" + sha + "/" + name + ".pt"


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def cache_candidates(name: str) -> list[Path]:
    """Official whisper download cache locations worth reusing."""
    default = Path(os.path.expanduser("~")) / ".cache"
    base = Path(os.environ.get("XDG_CACHE_HOME", str(default))) / "whisper"
    return [base / (name + ".pt")]


def download(url: str, destination: Path) -> None:
    request = urllib.request.Request(
        url, headers={"User-Agent": "UnipusAI-Helper/fetch-whisper"})
    with urllib.request.urlopen(request, timeout=180) as source, \
            destination.open("wb") as output:
        total = int(source.info().get("Content-Length") or 0)
        done = 0
        while True:
            buffer = source.read(1024 * 1024)
            if not buffer:
                break
            output.write(buffer)
            done += len(buffer)
            if total:
                print("\r  %.1f%% (%d/%d MB)" % (
                    done * 100 / total, done // 1048576, total // 1048576),
                    end="", flush=True)
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="base", choices=sorted(MODELS),
                        help="which whisper checkpoint to bundle (default: base)")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY,
                        help="base URL of the official model host")
    parser.add_argument("--source", default=None,
                        help="reuse an existing verified checkpoint instead of downloading")
    parser.add_argument("--force", action="store_true",
                        help="re-verify / re-download even if the target already exists")
    args = parser.parse_args()

    name = args.model
    sha, filename = MODELS[name]
    target_dir = ROOT / "whisper_models"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / filename

    def verified(path: Path) -> bool:
        return path.is_file() and sha256_of(path) == sha

    if not args.force and verified(target):
        print("Already present: " + str(target) + " (" +
              format(target.stat().st_size, ",") + " bytes)")
        return 0

    # 1) reuse a locally cached official checkpoint (seconds, no network)
    sources = ([Path(args.source)] if args.source else []) + cache_candidates(name)
    for src in sources:
        if verified(src):
            print("Reusing verified checkpoint: " + str(src))
            shutil.copy2(src, target)
            print("  " + format(target.stat().st_size, ",") + " bytes")
            return 0

    # 2) download from the official endpoints, with mirrors as fallback
    registries = [args.registry] + [m for m in MIRRORS if m != args.registry]
    tmp = target.with_suffix(target.suffix + ".part")
    for registry in registries:
        url = model_url(registry, name, sha)
        print("Downloading " + url)
        try:
            download(url, tmp)
            if verified(tmp):
                tmp.replace(target)
                print("Bundled Whisper model ready at " + str(target) +
                      " (" + format(target.stat().st_size, ",") + " bytes)")
                return 0
            print("  checksum mismatch, trying next mirror", file=sys.stderr)
        except (urllib.error.URLError, OSError) as exc:
            print("  download failed: " + str(exc) + ", trying next mirror",
                  file=sys.stderr)
        finally:
            if tmp.exists():
                tmp.unlink(missing_ok=True)
    print("ERROR: could not obtain a verified Whisper checkpoint", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
