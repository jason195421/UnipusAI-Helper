"""Locate the Whisper checkpoint shipped inside the application bundle.

The checkpoint lives at <bundle>/whisper_models/base.pt (PyInstaller copies it
there via the spec's datas).  Passing that directory as whisper.load_model's
download_root makes whisper reuse the file and skip its online download, so
voice features work offline right after installation.

Nothing here runs at import time.
"""
from __future__ import annotations

import sys
from pathlib import Path

from .paths import PROJECT_ROOT

MODEL_NAME = "base"
MODEL_FILE = "base.pt"
SUBDIR = "whisper_models"


def _candidate_roots():
    """Yield plausible bundle roots, most specific first (mirrors ffmpeg_runtime).

    On macOS, PyInstaller's BUNDLE relocates DATA files into Contents/Resources
    (cross-linked into Contents/Frameworks) while sys._MEIPASS points at
    Contents/MacOS.  Cover all three so the bundled model is found regardless
    of the exact PyInstaller version.
    """
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        yield Path(meipass)
    if getattr(sys, "frozen", False):
        exe = Path(sys.executable).resolve()
        yield exe.parent
        if sys.platform == "darwin":
            for parent in exe.parents:
                if parent.name == "Contents":
                    yield parent / "Resources"
                    yield parent / "Frameworks"
                    yield parent / "MacOS"
                    break
    yield PROJECT_ROOT


def bundled_whisper_dir() -> Path | None:
    """Return the directory holding the bundled checkpoint, or None."""
    for base in _candidate_roots():
        candidate = base / SUBDIR
        if (candidate / MODEL_FILE).is_file():
            return candidate
    return None


def bundled_whisper_model() -> Path | None:
    """Return the bundled checkpoint path, or None when it is not present."""
    directory = bundled_whisper_dir()
    return (directory / MODEL_FILE) if directory is not None else None
