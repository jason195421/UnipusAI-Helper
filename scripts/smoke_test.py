#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Headless smoke test for a built UnipusAI-Helper variant.

Launches the exe with QT_QPA_PLATFORM=offscreen for a short while. A healthy
build keeps running (the QML setup page enters app.exec()); a broken one exits
immediately with a traceback. Works for both console (debug) and windowed/GUI
(release) builds: in GUI mode stdio goes to logs/, which we scan for markers.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FATAL = ("Traceback (most recent call last)", "ModuleNotFoundError",
         "ReferenceError", "QML_LOAD_FAIL", "Fatal Python error")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["debug", "release"], required=True)
    ap.add_argument("--seconds", type=float, default=12.0)
    args = ap.parse_args()

    name = "UnipusAI-Helper" + ("-Debug" if args.mode == "debug" else "")
    if sys.platform == "darwin" and args.mode == "release":
        exe = ROOT / "dist" / "UnipusAI-Helper.app" / "Contents" / "MacOS" / "UnipusAI-Helper"
        logdir = Path.home() / "Library" / "Application Support" / "UnipusAI-Helper" / "logs"
    else:
        exe = ROOT / "dist" / name / (name + (".exe" if sys.platform == "win32" else ""))
        logdir = ROOT / "dist" / name / "logs"
    if not exe.is_file():
        raise SystemExit("[smoke] ERROR: exe not found: " + str(exe))

    env = os.environ.copy()
    env["QT_QPA_PLATFORM"] = "offscreen"
    env["SE_OFFLINE"] = "true"
    env["UNIPUS_GUI_NO_DIALOG"] = "1"
    env.setdefault("PYTHONUTF8", "1")

    if logdir.is_dir():
        for p in logdir.glob("*.log"):
            try:
                p.unlink()
            except OSError:
                pass

    print("[smoke] launching " + str(exe), flush=True)
    proc = subprocess.Popen([str(exe), "--skip-check"], cwd=str(exe.parent),
                            env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    try:
        out = proc.communicate(timeout=args.seconds)[0]
        early = True
    except subprocess.TimeoutExpired:
        early = False
        proc.terminate()
        try:
            out = proc.communicate(timeout=10)[0]
        except subprocess.TimeoutExpired:
            proc.kill()
            out = proc.communicate()[0]

    text = (out or b"").decode("utf-8", "replace")
    if logdir.is_dir():
        for p in sorted(logdir.glob("*.log")):
            try:
                text += "\n" + p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                pass

    for marker in FATAL:
        if marker in text:
            print("[smoke] FAIL marker: " + marker, flush=True)
            print(text[-4000:], flush=True)
            return 1
    if early:
        print("[smoke] FAIL: process exited too early (rc=%s)" % proc.returncode, flush=True)
        print(text[-4000:], flush=True)
        return 1
    print("[smoke] OK: survived %.0fs headless, no fatal markers" % args.seconds, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
