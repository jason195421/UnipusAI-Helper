"""Platform detection for the adaptive Qt Quick theme.

One QML codebase serves three looks:

* Windows  -> WinUI 3 / Fluent (Mica-like tint, rounded cards, Fluent blue)
* macOS    -> Aqua (vibrancy-like sidebar, system blue, PingFang SC)
* Linux    -> neutral dark fallback

The chosen palette is exposed to QML as a registered singleton
(import UnipusAI.Platform 1.0).  Values are resolved once at startup;
set UNIPUS_THEME=dark|light (or UNIPUS_ACCENT=#rrggbb) to override.
"""
from __future__ import annotations

import os
import subprocess
import sys

from PySide6.QtCore import Property, Qt
from PySide6.QtGui import QColor, QFontDatabase
from PySide6.QtQml import qmlRegisterSingletonInstance

URI = "UnipusAI.Platform"
TYPE_NAME = "PlatformInfo"


def is_windows() -> bool:
    return sys.platform == "win32"


def is_macos() -> bool:
    return sys.platform == "darwin"


def _registry_dword(path: str, name: str):
    if not is_windows():
        return None
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as key:
            value, _ = winreg.QueryValueEx(key, name)
            return int(value)
    except (OSError, ValueError, TypeError):
        return None


def _system_dark() -> bool:
    override = (os.environ.get("UNIPUS_THEME") or "").strip().lower()
    if override in ("dark", "1", "true"):
        return True
    if override in ("light", "0", "false"):
        return False

    if is_windows():
        # AppsUseLightTheme: 0 = dark apps, 1 = light apps.  Fall back to the
        # system-wide value, then to light (the Windows default).
        personalize = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        apps = _registry_dword(personalize, "AppsUseLightTheme")
        if apps is not None:
            return apps == 0
        system = _registry_dword(personalize, "SystemUsesLightTheme")
        if system is not None:
            return system == 0
        return False

    if is_macos():
        try:
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True, text=True, timeout=2,
            )
            return result.returncode == 0 and "dark" in result.stdout.lower()
        except (OSError, subprocess.SubprocessError):
            return False

    # Linux / other: prefer a dark GTK scheme, otherwise keep the neutral
    # dark palette the app has always shipped with.
    theme = (os.environ.get("GTK_THEME") or "").lower()
    if "light" in theme:
        return False
    try:
        result = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
            capture_output=True, text=True, timeout=2,
        )
        if result.returncode == 0 and "prefer-light" in result.stdout:
            return False
    except (OSError, subprocess.SubprocessError):
        pass
    return True


def default_accent(dark: bool) -> str:
    if is_windows():
        # WinUI 3 exposes a lighter accent on dark backgrounds for contrast.
        return "#60CDFF" if dark else "#0078D4"
    if is_macos():
        return "#0A84FF" if dark else "#007AFF"
    return "#77B4FF" if dark else "#0067C0"


def ui_font_family() -> str:
    try:
        families = set(QFontDatabase.families())
    except Exception:
        families = set()
    if is_windows():
        preferred = ("Microsoft YaHei UI", "Microsoft YaHei", "Segoe UI", "Noto Sans SC")
    elif is_macos():
        preferred = ("PingFang SC", "SF Pro Text", "Helvetica Neue", "Noto Sans SC")
    else:
        preferred = ("Noto Sans SC", "Source Han Sans SC", "DejaVu Sans")
    return next((name for name in preferred if name in families), "")


class PlatformInfo:
    """QML-facing, immutable description of the host platform."""

    def __init__(self, dark: bool | None = None, accent: str | None = None):
        self._dark = _system_dark() if dark is None else bool(dark)
        self._accent = (accent or os.environ.get("UNIPUS_ACCENT") or
                        default_accent(self._dark))
        self._family = ui_font_family()

    # -- getters -----------------------------------------------------------
    def _get_is_windows(self): return is_windows()
    def _get_is_macos(self): return is_macos()
    def _get_is_linux(self): return not (is_windows() or is_macos())
    def _get_dark(self): return self._dark
    def _get_accent(self): return QColor(self._accent)
    def _get_accent_hex(self): return self._accent
    def _get_family(self): return self._family
    def _get_theme_id(self):
        if is_windows():
            return "winui3-dark" if self._dark else "winui3-light"
        if is_macos():
            return "mac-dark" if self._dark else "mac-light"
        return "fluent-dark" if self._dark else "fluent-light"

    # PySide6 6.12 requires the decorator form; class-attribute Property
    # assignment silently yields false/empty values inside QML singletons.
    isWindows = Property(bool, _get_is_windows, constant=True)
    isMacOS = Property(bool, _get_is_macos, constant=True)
    isLinux = Property(bool, _get_is_linux, constant=True)
    dark = Property(bool, _get_dark, constant=True)
    accent = Property(QColor, _get_accent, constant=True)
    accentHex = Property(str, _get_accent_hex, constant=True)
    family = Property(str, _get_family, constant=True)
    themeId = Property(str, _get_theme_id, constant=True)

    def color_scheme(self):
        return Qt.ColorScheme.Dark if self._dark else Qt.ColorScheme.Light


_PLATFORM_INFO = None
_REGISTERED = False


def register_platform_theme(dark: bool | None = None, accent: str | None = None):
    """Register (once) the singleton and return it; keeps Python ownership."""
    global _PLATFORM_INFO, _REGISTERED
    if _PLATFORM_INFO is None:
        _PLATFORM_INFO = PlatformInfo(dark=dark, accent=accent)
    if not _REGISTERED:
        qmlRegisterSingletonInstance(
            PlatformInfo, URI, 1, 0, TYPE_NAME, _PLATFORM_INFO
        )
        _REGISTERED = True
    return _PLATFORM_INFO
