import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// Shared single-line input used by the built-in Settings page.
TextField {
    id: fieldControl
    Layout.fillWidth: true
    Layout.minimumWidth: 0
    implicitHeight: 36
    selectByMouse: true
    color: Theme.ink
    placeholderTextColor: Theme.muted
    font.family: Theme.fontFamily
    font.pixelSize: 13
    font.hintingPreference: Font.PreferFullHinting
    renderType: Text.NativeRendering
    leftPadding: 12
    rightPadding: 12
    background: Rectangle {
        radius: Theme.radiusSm
        color: Theme.raised
        border.width: 1
        border.color: fieldControl.activeFocus ? Theme.accent : Theme.line
    }
}
