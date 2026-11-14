# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for the UnipusAI-Helper config editor (onefile, windowed)."""
from PyInstaller.utils.hooks import collect_all

qfl_datas, qfl_binaries, qfl_hiddenimports = collect_all('qfluentwidgets')

a = Analysis(
    ['config_editor.py'],
    pathex=[],
    binaries=qfl_binaries,
    datas=qfl_datas,
    hiddenimports=[
        'unipus_helper.paths',
        'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets',
        'PyQt5.QtSvg', 'PyQt5.QtXml', 'PyQt5.QtMultimedia',
        'PyQt5.QtMultimediaWidgets',
        'qfluentwidgets', 'sip', 'pkgutil', 'winsound',
    ] + qfl_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PySide6', 'shiboken6', 'torch', 'numba', 'llvmlite',
        'whisper', 'tiktoken', 'edge_tts', 'openai', 'selenium',
        'numpy', 'PyQt5.QtWebEngine', 'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtQml', 'PyQt5.QtQuick', 'PyQt5.QtQuickWidgets',
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ConfigEditor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
