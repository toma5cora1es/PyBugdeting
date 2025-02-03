import sqlite3
import bcrypt  # pip install bcrypt

class DBManager:
    def __init__(self, db_name="budgets.db"):
        self.db_name = db_name
        self.connection = None
        self.create_connection()
        self.create_tables()             # Tablas básicas
        self.create_additional_tables()  # Tablas de las hojas extra

    def create_connection(self):
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None

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

        # Inserta usuarios de ejemplo si no existen
        cursor.execute("SELECT COUNT(*) as count FROM users")
        if cursor.fetchone()["count"] == 0:
            admin_hashed = self.hash_password("admin123")
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           ("admin", admin_hashed, "admin"))
            seller_hashed = self.hash_password("ventas123")
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           ("vendedor1", seller_hashed, "seller"))

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

    def create_additional_tables(self):
        cursor = self.connection.cursor()
        # VARIABLES
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS variables (
                valor_dolar TEXT,
                fecha TEXT,
                numero_presupuesto TEXT
            )
        """)

        # Kits Productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kits_productos (
                kit_producto_id TEXT,
                kit_id TEXT,
                precio_id TEXT,
                cantidad TEXT,
                envio_unitario TEXT
            )
        """)

        # Financiaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financiaciones (
                inactiva TEXT,
                descripcion TEXT,
                banco TEXT,
                tarjetas TEXT,
                dias_validos TEXT,
                cuotas TEXT,
                fecha_inicio TEXT,
                fecha_fin TEXT,
                estado TEXT
            )
        """)

        # Promociones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS promociones (
                promocion_id TEXT,
                descripcion TEXT,
                tipo_de_promocion TEXT,
                valor TEXT,
                fecha_inicio TEXT,
                fecha_fin TEXT,
                condiciones TEXT,
                estado TEXT
            )
        """)

        # Kits
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kits (
                kit_id TEXT,
                descripcion TEXT,
                imagen TEXT,
                folder_id TEXT
            )
        """)

        # MAPA_ARG
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mapa_arg (
                id TEXT,
                nombre TEXT,
                provincia_nombre TEXT,
                centroide_lon TEXT,
                centroide_lat TEXT
            )
        """)

        # Vendedores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendedores (
                vendedores_id TEXT,
                nombre TEXT,
                email TEXT
            )
        """)

        # Listas de Precios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS listas_de_precios (
                listadeprecio_id TEXT,
                margen_comercial TEXT,
                factor_extra TEXT,
                nombre TEXT,
                logo TEXT,
                orden_prioridad TEXT
            )
        """)

        # Presupuestos (hoja)
        # Presupuestos (hoja)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS presupuestos (
                presupuesto_id TEXT,
                cliente_id TEXT,
                proyecto_id TEXT,
                fecha_de_creacion TEXT,
                envio_total TEXT,
                kit_id TEXT,
                link TEXT,
                vendedor_id TEXT,
                estado_ejecucion TEXT,
                dispararproceso TEXT,
                aplicar_descuento_efectivo TEXT
            )
        """)

        # Detalles de Presupuestos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalles_de_presupuestos (
                detalle_id TEXT,
                presupuesto_id TEXT,
                precio_id TEXT,
                cantidad TEXT,
                envio_unitario TEXT,
                precio_en_pesos_manual TEXT,
                precio_en_dolares TEXT,
                iva TEXT,
                margen_comercial TEXT,
                descripcion_manual TEXT,
                comentario TEXT
            )
        """)

        # Clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cliente_id TEXT,
                nombre TEXT,
                ciudad TEXT,
                provincia TEXT,
                telefono TEXT,
                tipo_de_instalacion TEXT,
                cuit TEXT,
                id_mapa TEXT
            )
        """)

        # Productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                producto_id TEXT,
                precio_id TEXT,
                descripcion TEXT,
                tipo_de_producto TEXT,
                precio_en_pesos_manual TEXT,
                precio_dolares TEXT,
                iva TEXT,
                disponibilidad TEXT,
                margen_comercial TEXT
            )
        """)

        # Precios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS precios (
                precio_id TEXT,
                descripcion TEXT,
                precio_dolares TEXT,
                iva TEXT,
                disponibilidad TEXT,
                margen_comercial TEXT,
                listadeprecio_id TEXT,
                precio_en_pesos TEXT,
                margen_comercial_por_lista TEXT,
                factor_extra_para_descuento TEXT
            )
        """)

        # QUERY MULTIRADIO
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_multiradio (
                codigo TEXT,
                descripcion TEXT,
                precio TEXT,
                iva TEXT,
                disponibilidad TEXT,
                margen_comercial TEXT,
                listadeprecio_id TEXT,
                precio_en_pesos TEXT,
                margen_comercial_por_lista TEXT,
                factor_extra_para_descuento TEXT
            )
        """)

        # MULTIRADIO (usamos solo las columnas relevantes)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS multiradio (
                codigo TEXT,
                descripcion TEXT,
                iva TEXT,
                eliminado TEXT,
                precio_en_dolares TEXT,
                precio_por_metro TEXT,
                link TEXT
            )
        """)

        # QUERY G2E
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_g2e (
                codigo TEXT,
                descripcion TEXT,
                precio TEXT,
                iva TEXT,
                disponibilidad TEXT,
                margen_comercial TEXT,
                listadeprecio_id TEXT,
                precio_en_pesos TEXT
            )
        """)

        # G2E
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS g2e (
                precios TEXT,
                precio_por_panel TEXT,
                precio_formateado TEXT,
                link TEXT
            )
        """)

        # QUERY SILTRON
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_siltron (
                codigo TEXT,
                descripcion TEXT,
                precio TEXT,
                iva TEXT,
                disponibilidad TEXT,
                margen_comercial TEXT,
                listadeprecio_id TEXT,
                precio_en_pesos TEXT
            )
        """)

        # SILTRON
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS siltron (
                lista_de_precios_distribuidor TEXT,
                lista TEXT
            )
        """)

        # QUERY SOLARSOL
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_solarsol (
                codigo TEXT,
                descripcion TEXT,
                precio TEXT,
                iva TEXT,
                disponibilidad TEXT,
                margen_comercial TEXT,
                listadeprecio_id TEXT,
                precio_en_pesos TEXT
            )
        """)

        # SOLARSOL
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS solarsol (
                lista_de_precios_mayorista TEXT,
                septiembre TEXT,
                codigo TEXT,
                descripcion TEXT,
                iva TEXT
            )
        """)

        # QUERY WEGA
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_wega (
                codigo TEXT,
                descripcion TEXT,
                precio TEXT,
                iva TEXT,
                disponibilidad TEXT,
                margen_comercial TEXT,
                listadeprecio_id TEXT,
                precio_en_pesos TEXT
            )
        """)

        # WEGA
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wega (
                codigo TEXT,
                descripcion TEXT,
                precio_base TEXT,
                iva TEXT,
                stock TEXT,
                link TEXT
            )
        """)

        # QUERY YPF
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_ypf (
                codigo TEXT,
                descripcion TEXT,
                precio TEXT,
                iva TEXT,
                disponibilidad TEXT,
                margen_comercial TEXT,
                listadeprecio_id TEXT,
                precio_en_pesos TEXT
            )
        """)

        # YPF
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ypf (
                codigo_unico_solarsol TEXT,
                iva TEXT,
                precio TEXT,
                link TEXT
            )
        """)

        # Resumen Hojas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resumen_hojas (
                hoja TEXT,
                columna TEXT,
                nombre TEXT
            )
        """)
        self.connection.commit()

    # -- Manejo de contraseñas con hash --
    def hash_password(self, plain_text_password):
        return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, plain_text_password, hashed_password):
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)

    def login_user(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        row = cursor.fetchone()
        if row:
            stored_password = row["password"]
            if isinstance(stored_password, str):
                stored_password = stored_password.encode('utf-8')
            if self.check_password(password, stored_password):
                return row
        return None

    # -- Manejo de presupuestos --
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
