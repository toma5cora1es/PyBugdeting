import QtQuick 2.15
import QtQuick.Controls 2.15
import Styles 1.0
import Components 1.0

Button {
    id: root
    property alias buttonText: label.text
    property color buttonColor: StyleSettings.primaryColor

    contentItem: Text {
        id: label
        text: root.text
        font: StyleSettings.mainFont
        color: "white"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }

    background: Rectangle {
        color: root.buttonColor
        radius: 4
    }
}
