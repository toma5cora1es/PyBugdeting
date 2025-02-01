import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: root
    visible: true
    width: 800
    height: 600

    property string currentUser: ""
    property string currentRole: ""

    Loader {
        id: mainLoader
        anchors.fill: parent
        source: "Login.qml"
    }

    Connections {
        target: auth_manager
        function onLogged_in(role, username) {
            currentRole = role
            currentUser = username
            mainLoader.source = (role === "admin") ? "Dashboard.qml" : "BudgetEditor.qml"
        }
    }
}
