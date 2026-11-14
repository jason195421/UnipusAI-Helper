# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for UnipusAI-Helper (single onedir exe, console; settings built in)."""
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = [('unipus_helper/qml', 'unipus_helper/qml')]
datas += collect_data_files('whisper')
datas += collect_data_files('selenium')

hiddenimports = collect_submodules('unipus_helper')
# selenium 4.x 在 selenium/webdriver/__init__.py 用 __getattr__ + importlib.import_module
# 懒加载 webdriver.EdgeOptions / Edge / ActionChains / Keys 等（第 92-103 行），
# PyInstaller 静态分析发现不了这些动态导入，必须显式收集全部子模块，
# 否则运行时报 ModuleNotFoundError: No module named 'selenium.webdriver.edge.options'。
hiddenimports += collect_submodules('selenium')
hiddenimports += [
    'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtQml',
    'PySide6.QtQuick', 'PySide6.QtQuickControls2', 'shiboken6',
    'edge_tts', 'tiktoken_ext.openai_public', 'winreg', 'winsound',
    'whisper',
]

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
    console=True,
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
