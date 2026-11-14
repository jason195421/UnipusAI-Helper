pragma Singleton
import QtQuick
import UnipusAI.Platform 1.0

// One codebase, three platform-adaptive looks:
//   Windows  -> WinUI 3 / Fluent (Mica-tinted layers, Fluent blue, 8px corners)
//   macOS    -> Aqua (vibrant sidebar, system blue, 10-12px corners)
//   other    -> neutral Fluent dark/light fallback
// All colours and radii are exposed here; components must never hardcode them.
QtObject {
    readonly property bool dark: PlatformInfo.dark
    readonly property bool winui3: PlatformInfo.isWindows
    readonly property bool macos: PlatformInfo.isMacOS
    readonly property string themeId: PlatformInfo.themeId
    readonly property string fontFamily: PlatformInfo.family !== "" ? PlatformInfo.family : Qt.application.font.family

    // Accent follows the OS (Windows DWM / macOS system blue); UNIPUS_ACCENT overrides.
    readonly property color accent: PlatformInfo.accent
    readonly property color accentFill: PlatformInfo.accentFill
    readonly property color accentPressed: PlatformInfo.accentPressed
    readonly property color accentInk: "#ffffff"

    // Layer colours. WinUI 3 uses cool, slightly desaturated Mica tints;
    // macOS Aqua uses warmer light greys / graphite dark greys.
    readonly property color canvas: dark
        ? (winui3 ? "#202124" : macos ? "#1e1e20" : "#151517")
        : (winui3 ? "#f3f3f3" : macos ? "#ececec" : "#f5f5f7")
    readonly property color surface: dark
        ? (winui3 ? "#2b2b2e" : macos ? "#2a2a2c" : "#242426")
        : (winui3 ? "#ffffff" : macos ? "#ffffff" : "#ffffff")
    readonly property color sidebar: dark
        ? (winui3 ? "#27272a" : macos ? "#232325" : "#222224")
        : (winui3 ? "#eef0f4" : macos ? "#e8e8ea" : "#eef0f4")
    readonly property color raised: dark
        ? (winui3 ? "#323236" : macos ? "#323234" : "#2c2c2f")
        : (winui3 ? "#f7f8fa" : macos ? "#f5f5f7" : "#f0f0f2")
    readonly property color hover: dark
        ? (winui3 ? "#3a3a40" : macos ? "#3a3a3c" : "#343437")
        : (winui3 ? "#e4e7ec" : macos ? "#e2e2e5" : "#e4e7ec")
    readonly property color line: dark
        ? (winui3 ? "#45454b" : macos ? "#454547" : "#3d3d41")
        : (winui3 ? "#d6d9df" : macos ? "#d5d5d8" : "#d8d8dc")
    readonly property color subtleLine: dark
        ? (winui3 ? "#353539" : macos ? "#353537" : "#303034")
        : (winui3 ? "#e6e8ec" : macos ? "#e2e2e5" : "#e8e8ec")

    readonly property color ink: dark ? "#f4f4f6" : (winui3 ? "#1b1b1f" : macos ? "#1d1d1f" : "#1b1b1f")
    readonly property color secondary: dark ? "#d1d1d6" : (winui3 ? "#5b5f67" : macos ? "#6e6e73" : "#5b5f67")
    readonly property color muted: dark ? "#a8a8b0" : (winui3 ? "#8a8f98" : macos ? "#8e8e93" : "#8a8f98")

    readonly property color navigation: dark ? "#243a56" : (winui3 ? "#dce7f5" : macos ? "#d6e6f7" : "#dce7f5")
    readonly property color selection: dark ? "#263346" : (winui3 ? "#e3ecf7" : macos ? "#dfeaf7" : "#e3ecf7")
    readonly property color selectionHover: dark ? "#30415a" : (winui3 ? "#d3e1f2" : macos ? "#cfe0f2" : "#d3e1f2")
    readonly property color selectionLine: dark ? "#3d506a" : (winui3 ? "#b9cfeb" : macos ? "#b3cbe9" : "#b9cfeb")
    readonly property color track: dark ? "#4a4a50" : "#d8d8de"

    readonly property color success: dark ? "#b4e2c2" : (macos ? "#1a7f3c" : "#0f7b3f")
    readonly property color successSurface: dark ? "#22442d" : (macos ? "#e3f5e8" : "#e6f4ea")
    readonly property color error: dark ? "#f0aaa5" : "#c42b1c"
    readonly property color warning: dark ? "#e2bf86" : "#9d5d00"
    readonly property color compulsory: dark ? "#ffb04d" : "#b35c00"
    readonly property color requiredInk: dark ? "#24180c" : "#ffffff"

    // Corner radii: WinUI 3 favours 4-8px, macOS 8-12px.
    readonly property int radiusXs: winui3 ? 4 : 5
    readonly property int radiusSm: winui3 ? 6 : 8
    readonly property int radiusMd: winui3 ? 8 : (macos ? 12 : 10)
    readonly property int radiusLg: winui3 ? 12 : (macos ? 16 : 14)

    // Mica / Aqua window backdrop (used by Main.qml ApplicationWindow.background).
    readonly property color windowTop: dark
        ? (winui3 ? "#2a2d3a" : macos ? "#26262b" : "#1b1b20")
        : (winui3 ? "#dfe6f2" : macos ? "#f2eee9" : "#eef1f8")
    readonly property color windowBottom: canvas
    readonly property color sidebarTop: dark
        ? (winui3 ? "#2b2f3d" : macos ? "#262629" : "#252528")
        : (winui3 ? "#e7ecf6" : macos ? "#eeeae4" : "#f0f2f8")
    readonly property color sidebarBottom: sidebar
    readonly property real sidebarOpacity: dark ? 0.92 : (macos ? 0.82 : 0.88)
    readonly property int sidebarBorder: winui3 ? 1 : 0
}
