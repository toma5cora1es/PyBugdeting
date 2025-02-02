import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtCharts 2.15
import Styles 1.0


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
    source: "views/Login.qml"
    }

    Connections {
        target: auth_manager
        function onLogged_in(role, username) {
            currentRole = role
            currentUser = username
            mainLoader.source = (role === "admin") ? "views/Dashboard.qml" : "views/BudgetEditor.qml"
        }
    }
}
