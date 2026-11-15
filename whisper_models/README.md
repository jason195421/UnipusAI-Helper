# 内置 Whisper 模型

`base.pt` 由 `python scripts/fetch_whisper.py` 在构建前下载（或复用本机
whisper 缓存中已校验的副本），随安装包经 PyInstaller `datas` 内置到
`whisper_models/base.pt`。运行时 `unipus_helper/whisper_runtime.py` 定位该目录，
并把它作为 `download_root` 传给 `whisper.load_model("base", ...)`：文件 SHA256
与官方 URL 内嵌的校验值一致，whisper 会直接复用本地文件，首次启动无需联网
下载约 145 MB 的模型权重。

该目录内容体积大、不进版本库（见 `.gitignore`），只保留本说明。
