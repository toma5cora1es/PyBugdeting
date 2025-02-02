import QtQuick 2.15
import QtCharts 2.15
import Styles 1.0
import Components 1.0


Item {
    property var chartData: []

    ChartView {
        anchors.fill: parent
        antialiasing: true

        BarSeries {
            axisX: BarCategoryAxis { categories: ["Ene", "Feb", "Mar"] }
            BarSet { values: chartData }
        }
    }
}