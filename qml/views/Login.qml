import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import Styles 1.0
import Components 1.0

Rectangle {
    id: loginRoot
    color: StyleSettings.backgroundColor

    // Exponemos un método para mostrar error
    function showError(msg) {
        errorLabel.text = msg
        errorLabel.visible = true
    }

    ColumnLayout {
        anchors.centerIn: parent
        spacing: StyleSettings.spacingUnit * 2

        Text {
            text: "Inicio de Sesión"
            font.bold: true
            font.pixelSize: StyleSettings.mainFont.pixelSize * 1.5
            color: StyleSettings.primaryColor
            Layout.alignment: Qt.AlignHCenter
        }

        // Mensaje de error
        Text {
            id: errorLabel
            text: ""
            color: "red"
            visible: false
            Layout.alignment: Qt.AlignHCenter
        }

        TextField {
            id: usernameField
            placeholderText: "Usuario"
            font: StyleSettings.mainFont
            color: StyleSettings.textColor
            Layout.fillWidth: true
        }

        TextField {
            id: passwordField
            placeholderText: "Contraseña"
            echoMode: TextInput.Password
            font: StyleSettings.mainFont
            color: StyleSettings.textColor
            Layout.fillWidth: true
        }

        CustomButton {
            buttonText: "Iniciar Sesión"
            Layout.alignment: Qt.AlignHCenter
            onClicked: {
                errorLabel.visible = false
                auth_manager.login(usernameField.text, passwordField.text)
            }
        }
    }
}
