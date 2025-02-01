import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    color: "#f0f0f0"
    anchors.fill: parent

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 15

        TextField {
            id: usernameField
            placeholderText: "Usuario"
        }

        TextField {
            id: passwordField
            placeholderText: "Contraseña"
            echoMode: TextInput.Password
        }

        Button {
            text: "Iniciar Sesión"
            onClicked: auth_manager.login(usernameField.text, passwordField.text)
        }
    }
}
