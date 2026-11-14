"""Locate the FFmpeg binaries shipped inside the application bundle.

The binaries live at <bundle>/ffmpeg/<platform-id>/ (PyInstaller copies them
there via the spec's datas).  Whisper's load_audio simply calls
subprocess.run(["ffmpeg", ...]), so prepending that directory to PATH is
enough to make both Whisper and EnvironmentChecker pick up the bundled tools
without any network access at first launch.

Nothing here runs at import time: call ensure_ffmpeg_on_path() early in
startup (and again defensively from EnvironmentChecker).
"""
from __future__ import annotations

import os
import platform
import sys
from pathlib import Path

from .paths import PROJECT_ROOT

_EXE = ".exe" if sys.platform == "win32" else ""


def platform_id() -> str:
    """Return the directory name used for this platform's bundled binaries."""
    system = sys.platform
    machine = (platform.machine() or "").lower()
    arm = machine in ("arm64", "aarch64")
    if system == "win32":
        return "win32-arm64" if arm else "win32-x64"
    if system == "darwin":
        return "darwin-arm64" if arm else "darwin-x64"
    return "linux-arm64" if arm else "linux-x64"


def _candidate_roots():
    """Yield plausible bundle roots, most specific first.

    On macOS, PyInstaller's BUNDLE relocates DATA files into
    Contents/Resources (cross-linked into Contents/Frameworks) while
    sys._MEIPASS points at Contents/MacOS.  Cover all three locations so the
    bundled FFmpeg is found regardless of the exact PyInstaller version.
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


def bundled_ffmpeg_dir() -> Path | None:
    """Return the directory containing the bundled ffmpeg/ffprobe, or None."""
    rel = Path("ffmpeg") / platform_id()
    for base in _candidate_roots():
        candidate = base / rel
        if (candidate / ("ffmpeg" + _EXE)).is_file():
            return candidate
    return None


def _ensure_executable(directory: Path) -> bool:
    """Make sure the bundled ffmpeg/ffprobe are executable; True on success."""
    for name in ("ffmpeg", "ffprobe"):
        binary = directory / name
        try:
            mode = binary.stat().st_mode
            if not (mode & 0o111):
                binary.chmod(mode | 0o755)
            if not os.access(str(binary), os.X_OK):
                return False
        except OSError:
            return False
    return True


def _writable_copy(directory: Path) -> Path | None:
    """Copy the bundled binaries into a writable temp dir and chmod them."""
    import shutil
    import tempfile

    fallback = Path(tempfile.gettempdir()) / ("unipus_ffmpeg_" + platform_id())
    try:
        fallback.mkdir(parents=True, exist_ok=True)
        for name in ("ffmpeg", "ffprobe"):
            source = directory / name
            if not source.is_file():
                return None
            target = fallback / name
            if not target.is_file() or target.stat().st_size != source.stat().st_size:
                shutil.copyfile(source, target)
            target.chmod(0o755)
        return fallback
    except OSError:
        return None


def ensure_ffmpeg_on_path() -> Path | None:
    """Prepend the bundled FFmpeg directory to PATH (idempotent).

    Returns the directory on success, or None when no bundled binaries are
    present (e.g. a source checkout before scripts/fetch_ffmpeg.py ran), in
    which case the pre-existing system FFmpeg is left untouched.
    """
    directory = bundled_ffmpeg_dir()
    if directory is None:
        return None

    # npm tarballs do not preserve the executable bit on Unix; repair it so a
    # freshly unpacked macOS/Linux bundle works without a manual chmod.  A
    # signed .app is read-only, so if the bit cannot be set (or the binary is
    # still not executable), fall back to a writable copy in the temp dir.
    if _EXE == "":
        if not _ensure_executable(directory):
            directory = _writable_copy(directory) or directory

    resolved = str(directory.resolve())
    current = os.environ.get("PATH", "")
    parts = [p for p in current.split(os.pathsep) if p]
    if not any(os.path.normcase(p) == os.path.normcase(resolved) for p in parts):
        os.environ["PATH"] = resolved + (os.pathsep + current if current else "")
    os.environ["UNIPUS_FFMPEG_DIR"] = resolved
    return directory
