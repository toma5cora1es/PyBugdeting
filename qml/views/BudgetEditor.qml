import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import Styles 1.0
import Components 1.0

Page {
    title: qsTr("Editor de Presupuestos")
    background: Rectangle {
        color: StyleSettings.backgroundColor
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: StyleSettings.spacingUnit * 2


        // Sección de entrada de datos
        RowLayout {
            Layout.fillWidth: true
            spacing: StyleSettings.spacingUnit
            TextField {
                id: clientName
                placeholderText: "Nombre del cliente"
                implicitWidth: parent.width / 2
                font: StyleSettings.mainFont
                color: StyleSettings.textColor
            }
            CustomButton {
                buttonText: "Crear nuevo presupuesto"
                Layout.alignment: Qt.AlignVCenter
                onClicked: {
                    if (clientName.text !== "") {
                        budget_manager.create_budget(clientName.text, "vendedor1")
                    }
                }
            }
        }

        // Lista de ítems del presupuesto
        ListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: budget_manager.items
            delegate: RowLayout {
                width: parent.width
                spacing: StyleSettings.spacingUnit
                Text {
                    text: model.description
                    Layout.fillWidth: true
                    font: StyleSettings.mainFont
                    color: StyleSettings.textColor
                }
                Text {
                    text: "$" + model.price.toFixed(2)
                    font: StyleSettings.mainFont
                    color: StyleSettings.primaryColor
                }
            }
        }

        // Sección para añadir nuevos ítems
        RowLayout {
            Layout.fillWidth: true
            spacing: StyleSettings.spacingUnit
            TextField {
                id: itemDescription
                placeholderText: "Descripción"
                Layout.fillWidth: true
                font: StyleSettings.mainFont
                color: StyleSettings.textColor
            }
            TextField {
                id: itemPrice
                placeholderText: "Precio"
                Layout.preferredWidth: 100
                font: StyleSettings.mainFont
                color: StyleSettings.textColor
            }
            CustomButton {
                buttonText: "Añadir"
                onClicked: {
                    let priceVal = parseFloat(itemPrice.text);
                    if (!isNaN(priceVal)) {
                        budget_manager.add_item(itemDescription.text, priceVal);
                        itemDescription.text = "";
                        itemPrice.text = "";
                    }
                }
            }
        }

        // Mostrar total del presupuesto
        Text {
            text: "Total: $" + budget_manager.total.toFixed(2)
            Layout.alignment: Qt.AlignHCenter
            font.bold: true
            color: StyleSettings.primaryColor
        }
    }
}