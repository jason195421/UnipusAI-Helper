# 内置 FFmpeg / ffprobe

语音转写（Whisper）通过 subprocess.run(["ffmpeg", ...]) 调用 ffmpeg，**不需要**
用户另行安装 FFmpeg：程序启动时会把随包内置的二进制目录加入 PATH
（见 unipus_helper/ffmpeg_runtime.py）。

## 目录结构

    ffmpeg/
      win32-x64/     Windows x64（ffmpeg.exe / ffprobe.exe）
      darwin-arm64/  macOS Apple Silicon（ffmpeg / ffprobe）
      darwin-x64/    macOS Intel
      linux-x64/     Linux x64（可选）

二进制**不进 git**（.gitignore 已忽略 ffmpeg/*/），由构建流程生成：

    # 本机（默认走 npmmirror 镜像，国内可达）
    python scripts/fetch_ffmpeg.py

    # GitHub Actions macOS runner（走官方 npm registry）
    python scripts/fetch_ffmpeg.py --registry https://registry.npmjs.org

## 来源

来自 npm 包 @ffmpeg-installer/<platform> 与 @ffprobe-installer/<platform>
（独立、静态链接的可执行文件）。版本映射见 scripts/fetch_ffmpeg.py 的
PACKAGES 字典。Windows 打包 spec 会把当前平台的目录原样收集到
_MEIPASS/ffmpeg/<platform-id>/。

## 验证

    python -c "from unipus_helper.ffmpeg_runtime import ensure_ffmpeg_on_path; import shutil; print(ensure_ffmpeg_on_path()); print(shutil.which('ffmpeg'))"

若内置目录缺失（例如只拉了源码没跑脚本），程序会回退到系统 PATH 中的
ffmpeg，原有的环境检查/自动安装流程仍作为兜底保留。
