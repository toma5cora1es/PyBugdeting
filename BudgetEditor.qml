import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Page {
    title: qsTr("Editor de Presupuestos")

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        TextField {
            id: clientName
            placeholderText: "Nombre del cliente"
        }

        Button {
            text: "Crear nuevo presupuesto"
            onClicked: {
                if (clientName.text !== "") {
                    // Pasa el usuario real en vez de Qt.application.arguments[0] si procede
                    budget_manager.create_budget(clientName.text, "vendedor1")
                }
            }
        }

        // ListView para los items
        ListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: budget_manager

            delegate: RowLayout {
                Layout.fillWidth: true
                spacing: 20

                Label {
                    // modelData para el primer rol si fuera role 0
                    text: model.description
                    // también podría ser text: modelData si sólo un rol
                }
                Label {
                    text: " $ " + model.price
                }
            }
        }

        RowLayout {
            TextField { id: itemDescription; placeholderText: "Descripción" }
            TextField { id: itemPrice; placeholderText: "Precio" }
            Button {
                text: "Añadir"
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

        Label {
            // Debido a que ahora "total" sí es float, QML puede invocar .toFixed()
            text: "Total: $" + budget_manager.total.toFixed(2)
            font.bold: true
        }
    }
}
