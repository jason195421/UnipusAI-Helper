# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for UnipusAI-Helper (single onedir exe, console; settings built in)."""
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os
import platform as _platform
import sys as _sys


def _ffmpeg_platform_id():
    """返回本次构建要内置的 ffmpeg/<id> 目录（与 ffmpeg_runtime.platform_id 一致）。"""
    if _sys.platform == "win32":
        return "win32-x64"
    if _sys.platform == "darwin":
        return "darwin-arm64" if _platform.machine() == "arm64" else "darwin-x64"
    machine = _platform.machine().lower()
    if machine in ("aarch64", "arm64"):
        return "linux-arm64"
    return "linux-x64"


datas = [('unipus_helper/qml', 'unipus_helper/qml')]
datas += collect_data_files('whisper')
datas += collect_data_files('selenium')

# 内置 FFmpeg：把对应平台的 ffmpeg/ffprobe 二进制原样收进 _MEIPASS，
# 运行时由 unipus_helper.ffmpeg_runtime 注入 PATH，首次启动无需联网下载。
# 该目录由 scripts/fetch_ffmpeg.py 或 GitHub Actions 在构建前生成（不进 git）。
_ffmpeg_id = _ffmpeg_platform_id()
_ffmpeg_dir = os.path.join('ffmpeg', _ffmpeg_id)
if os.path.isdir(_ffmpeg_dir):
    datas.append((_ffmpeg_dir, 'ffmpeg/' + _ffmpeg_id))
else:
    print('[spec] WARNING: 未找到 ' + _ffmpeg_dir + '，请先运行 scripts/fetch_ffmpeg.py --platform ' + _ffmpeg_id)

hiddenimports = collect_submodules('unipus_helper')
# selenium 4.x 在 selenium/webdriver/__init__.py 用 __getattr__ + importlib.import_module
# 懒加载 webdriver.EdgeOptions / Edge / ActionChains / Keys 等（第 92-103 行），
# PyInstaller 静态分析发现不了这些动态导入，必须显式收集全部子模块，
# 否则运行时报 ModuleNotFoundError: No module named 'selenium.webdriver.edge.options'。
hiddenimports += collect_submodules('selenium')
hiddenimports += [
    'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtQml',
    'PySide6.QtQuick', 'PySide6.QtQuickControls2', 'shiboken6',
    'edge_tts', 'tiktoken_ext.openai_public', 'whisper',
]
# winreg / winsound only exist on Windows; keep them platform-gated.
if _sys.platform == 'win32':
    hiddenimports += ['winreg', 'winsound']

a = Analysis(
    ['UnipusAI_Helper.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # 配置编辑已合并进主程序的 PySide6 / QML 设置页；旧版 PyQt5 编辑器不再打包。
    excludes=['PyQt5', 'qfluentwidgets'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='UnipusAI-Helper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=(_sys.platform != 'darwin'),
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='UnipusAI-Helper',
)

# A real .app bundle is only meaningful on macOS.  On Windows this block is
# skipped entirely, so the existing onedir + console build is unchanged.
if _sys.platform == "darwin":
    from PyInstaller.building.osx import BUNDLE

    app = BUNDLE(
        coll,
        name='UnipusAI-Helper.app',
        icon=None,
        bundle_identifier='com.jason195421.unipusai-helper',
        version='3.9.9',
        info_plist={
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '11.0',
            'CFBundleDisplayName': 'UnipusAI-Helper',
        },
    )
