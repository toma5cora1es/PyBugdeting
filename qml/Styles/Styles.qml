pragma Singleton
import QtQuick 2.15


QtObject {
    property color primaryColor: "#2A5CAA"
    property color secondaryColor: "#FF6B6B"
    property color backgroundColor: "#F5F7FB"
    property color textColor: "#333333"
    property int spacingUnit: 8
    property font mainFont: Qt.font({ family: "Inter", pixelSize: 14 })
}