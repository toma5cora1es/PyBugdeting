import QtQuick 2.15
import QtQuick.Layouts 1.15
import Styles 1.0
import Components 1.0


Rectangle {
    property alias title: titleText.text
    property alias total: totalText.text

    width: 200
    height: 100
    radius: 8
    color: StyleSettings.backgroundColor

    ColumnLayout {
        anchors.fill: parent
        spacing: StyleSettings.spacingUnit

        Text {
            id: titleText
            font.bold: true
            color: StyleSettings.textColor
        }

        Text {
            id: totalText
            color: StyleSettings.primaryColor
        }
    }
}