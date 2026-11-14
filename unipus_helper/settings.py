# -*- coding: utf-8 -*-
"""Configuration storage for the workbench's built-in Settings page.

The standalone PyQt5 / Fluent Widgets editor (config_editor.py) has been
superseded: config.json is now read and written through this PySide6 QObject,
exposed to QML as the "settings" context property, so the whole product
ships as one program, one window and one process.
"""
from __future__ import annotations

import json

from PySide6.QtCore import Property, QObject, Signal, Slot

from .paths import PROJECT_ROOT

CONFIG_PATH = PROJECT_ROOT / "config.json"

DEFAULT_CONFIG = {
    "username": "",
    "password": "",
    "url": "https://uai.unipus.cn/sso/index.html?service=https%3A%2F%2Fucloud.unipus.cn%2Fhome",
    "token_full": "",
    "api_key": "",
    "base_url": "",
    "model": "",
    "max_tokens": 32768,
    "temperature": 0.3,
    "debug_mode": False,
    # 录音题（Exercise 2 这类主观题）没有原声，需要 TTS 生成语音
    "tts_engine": "auto",   # auto / edge / sapi / off
    "tts_voice": "",
    "tts_proxy": "",
}

STRING_FIELDS = (
    "username", "password", "url", "token_full", "api_key", "base_url",
    "model", "tts_engine", "tts_voice", "tts_proxy",
)


def load_config():
    """Defaults merged with the on-disk config.json; never raises."""
    cfg = dict(DEFAULT_CONFIG)
    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, dict):
            cfg.update(data)
    except (OSError, ValueError, TypeError):
        pass
    return cfg


def _as_text(value, default=""):
    return default if value is None else str(value)


def _clean_token(value):
    token = _as_text(value).strip()
    if len(token) >= 2 and (
        (token[0] == "'" and token[-1] == "'")
        or (token[0] == '"' and token[-1] == '"')
    ):
        token = token[1:-1].strip()
    return token


def normalize_config(data):
    """Coerce values coming from QML (QVariantMap) into the on-disk schema."""
    if not isinstance(data, dict):
        data = {}
    out = dict(DEFAULT_CONFIG)
    for key in STRING_FIELDS:
        out[key] = _as_text(data.get(key, DEFAULT_CONFIG[key]))
    out["token_full"] = _clean_token(data.get("token_full", ""))
    try:
        out["max_tokens"] = int(float(data.get("max_tokens", DEFAULT_CONFIG["max_tokens"])))
    except (TypeError, ValueError):
        out["max_tokens"] = DEFAULT_CONFIG["max_tokens"]
    try:
        out["temperature"] = float(data.get("temperature", DEFAULT_CONFIG["temperature"]))
    except (TypeError, ValueError):
        out["temperature"] = DEFAULT_CONFIG["temperature"]
    value = data.get("debug_mode", False)
    out["debug_mode"] = value is True or (
        isinstance(value, str) and value.casefold() == "true"
    )
    return out


def save_config(data):
    """Write config.json next to the executable. Raises on IO errors."""
    out = normalize_config(data)
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CONFIG_PATH.open("w", encoding="utf-8") as handle:
        json.dump(out, handle, indent=2, ensure_ascii=False)
    return True


def is_config_ready():
    """True when the minimum credential needed to boot the bot is present."""
    return bool(_as_text(load_config().get("api_key")).strip())


class SettingsBridge(QObject):
    """Exposes config.json to QML as the "settings" context property."""

    saved = Signal()
    failed = Signal(str)

    def __init__(self, parent=None, setup_mode=False):
        super().__init__(parent)
        self._setup_mode = bool(setup_mode)

    @Property(bool, constant=True)
    def setupMode(self):
        return self._setup_mode

    @Slot(result="QVariantMap")
    def load(self):
        return load_config()

    @Slot("QVariantMap", result=bool)
    def save(self, data):
        if not isinstance(data, dict):
            self.failed.emit("配置数据格式无效")
            return False
        try:
            save_config(data)
        except Exception as exc:
            self.failed.emit(str(exc))
            return False
        self.saved.emit()
        return True

    @Slot(result=bool)
    def isReady(self):
        return is_config_ready()
