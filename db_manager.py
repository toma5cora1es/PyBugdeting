import sqlite3
import os

class DBManager:
    def __init__(self, db_name="budgets.db"):
        self.db_name = db_name
        self.connection = None
        self.create_connection()
        self.create_tables()

    def create_connection(self):
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row

    def create_tables(self):
        cursor = self.connection.cursor()

        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        # Insertar usuarios de ejemplo si no existen
        cursor.execute("SELECT COUNT(*) as count FROM users")
        if cursor.fetchone()["count"] == 0:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           ("admin", "admin123", "admin"))
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           ("vendedor1", "ventas123", "seller"))

        # Tabla de presupuestos (encabezado)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT NOT NULL,
                total REAL DEFAULT 0.0,
                created_by TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabla de ítems del presupuesto
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budget_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                budget_id INTEGER,
                description TEXT,
                price REAL,
                FOREIGN KEY(budget_id) REFERENCES budgets(id) ON DELETE CASCADE
            )
        """)

        self.connection.commit()

    def login_user(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM users WHERE username=? AND password=?
        """, (username, password))
        return cursor.fetchone()

    def create_budget(self, client_name, created_by):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO budgets (client_name, created_by) VALUES (?, ?)
        """, (client_name, created_by))
        self.connection.commit()
        return cursor.lastrowid

    def add_budget_item(self, budget_id, description, price):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO budget_items (budget_id, description, price) 
            VALUES (?, ?, ?)
        """, (budget_id, description, price))
        self.connection.commit()

    def get_budget_items(self, budget_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM budget_items WHERE budget_id=?
        """, (budget_id,))
        return cursor.fetchall()

    def get_budget_total(self, budget_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT SUM(price) as total FROM budget_items WHERE budget_id=?
        """, (budget_id,))
        row = cursor.fetchone()
        return row["total"] if row["total"] else 0.0

    def update_budget_total(self, budget_id, new_total):
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE budgets SET total=? WHERE id=?
        """, (new_total, budget_id))
        self.connection.commit()
