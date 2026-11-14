# PyInstaller runtime hook for release (windowed / GUI) builds.
# It runs before UnipusAI_Helper.py, so the stdio bootstrap there sees
# UNIPUS_GUI=1 and redirects stdio into logs/ even on platforms where the
# bootloader still hands us a stream (e.g. a macOS .app launched from Finder).
# Debug builds do NOT install this hook (see UnipusAI-Helper.spec).
import os
os.environ.setdefault("UNIPUS_GUI", "1")
