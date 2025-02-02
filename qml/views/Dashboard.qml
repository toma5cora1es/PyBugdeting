import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import Styles 1.0
import Components 1.0

Page {
    title: qsTr("Dashboard Admin")

    ColumnLayout {
        anchors.fill: parent
        spacing: StyleSettings.spacingUnit

        BudgetCard {
            title: "Presupuesto Total"
            total: "$" + budget_manager.total.toFixed(2)
        }

        ChartCard {
            Layout.fillWidth: true
            Layout.fillHeight: true
            chartData: [120, 200, 150]
        }
    }
}