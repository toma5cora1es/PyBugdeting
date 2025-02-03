import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import (QObject, pyqtSignal, pyqtSlot, QAbstractListModel,
                          QModelIndex, Qt, pyqtProperty)
from db_manager import DBManager

class AuthManager(QObject):
    logged_in = pyqtSignal(str, str)   # role, username
    login_failed = pyqtSignal()        # señal para avisar a QML del fallo

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager

    @pyqtSlot(str, str)
    def login(self, username, password):
        user = self.db_manager.login_user(username, password)
        if user:
            self.logged_in.emit(user["role"], user["username"])
        else:
            self.login_failed.emit()

class BudgetManager(QAbstractListModel):
    totalChanged = pyqtSignal(float)

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
            return item["price"]
        return None

    @pyqtProperty(float, notify=totalChanged)
    def total(self):
        return self._total

    @pyqtSlot(str, str)
    def create_budget(self, client_name, username):
        budget_id = self.db_manager.create_budget(client_name, username)
        self._current_budget_id = budget_id

        # Reset del modelo
        self.beginResetModel()
        self._items.clear()
        self.endResetModel()

        # Reset total
        self._total = 0.0
        self.totalChanged.emit(self._total)

    @pyqtSlot(str, float)
    def add_item(self, description, price):
        if self._current_budget_id is None:
            return

        self.beginInsertRows(QModelIndex(), len(self._items), len(self._items))
        self._items.append({"description": description, "price": price})
        self.endInsertRows()

        self.db_manager.add_budget_item(self._current_budget_id, description, price)

        new_total = self.db_manager.get_budget_total(self._current_budget_id)
        self.db_manager.update_budget_total(self._current_budget_id, new_total)
        self._total = new_total
        self.totalChanged.emit(self._total)

if __name__ == "__main__":
    # (Opcional) Si quieres limpiar la BD anterior para evitar 'Invalid salt':
    # if os.path.exists("budgets.db"):
    #     os.remove("budgets.db")

    app = QApplication(sys.argv)

    os.environ["QML2_IMPORT_PATH"] = os.path.join(os.path.dirname(__file__), "qml")
    print("QML Import Paths:", os.environ["QML2_IMPORT_PATH"])

    engine = QQmlApplicationEngine()

    db = DBManager()
    auth_manager = AuthManager(db)
    budget_manager = BudgetManager(db)

    engine.rootContext().setContextProperty("auth_manager", auth_manager)
    engine.rootContext().setContextProperty("budget_manager", budget_manager)

    engine.load(os.path.abspath("qml/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    exit_code = app.exec_()
    db.close_connection()
    sys.exit(exit_code)
