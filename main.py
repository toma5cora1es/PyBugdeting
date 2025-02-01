import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import (QObject, pyqtSignal, pyqtSlot, QAbstractListModel,
                          QModelIndex, Qt, pyqtProperty)
from db_manager import DBManager

class AuthManager(QObject):
    logged_in = pyqtSignal(str, str)  # role, username

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager

    @pyqtSlot(str, str) 
    def login(self, username, password):
        user = self.db_manager.login_user(username, password)
        if user:
            self.logged_in.emit(user["role"], user["username"])

class BudgetManager(QAbstractListModel):
    totalChanged = pyqtSignal(float)  # señal para notificar a QML

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self._items = []
        self._current_budget_id = None
        self._total = 0.0

    def roleNames(self):
        return {
            0: b"description",
            1: b"price"
        }

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        item = self._items[index.row()]
        if role == 0:
            return item["description"]
        elif role == 1:
            # Devolvemos solo el número, QML decide cómo mostrarlo
            return item["price"]
        return None

    # Exponer "total" como una Q_PROPERTY para que QML pueda llamarle .toFixed(2)
    @pyqtProperty(float, notify=totalChanged)
    def total(self):
        return self._total

    @pyqtSlot(str, str)
    def create_budget(self, client_name, username):
        budget_id = self.db_manager.create_budget(client_name, username)
        self._current_budget_id = budget_id
        self._items.clear()
        self.beginResetModel()
        self.endResetModel()

        self._total = 0.0
        self.totalChanged.emit(self._total)

    @pyqtSlot(str, float)
    def add_item(self, description, price):
        if self._current_budget_id is None:
            return

        # Insertar en modelo para QML
        self.beginInsertRows(QModelIndex(), len(self._items), len(self._items))
        self._items.append({"description": description, "price": price})
        self.endInsertRows()

        # Guardar en BD
        self.db_manager.add_budget_item(self._current_budget_id, description, price)

        # Obtener y actualizar total
        new_total = self.db_manager.get_budget_total(self._current_budget_id)
        self.db_manager.update_budget_total(self._current_budget_id, new_total)

        self._total = new_total
        self.totalChanged.emit(self._total)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    db = DBManager()
    auth_manager = AuthManager(db)
    budget_manager = BudgetManager(db)

    engine.rootContext().setContextProperty("auth_manager", auth_manager)
    engine.rootContext().setContextProperty("budget_manager", budget_manager)

    engine.load(QUrl("main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
