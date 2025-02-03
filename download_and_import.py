import csv
import os
import unicodedata
from db_manager import DBManager


def normalize_string(s):
    """
    Convierte la cadena s a minúsculas, reemplaza espacios y barras por guiones bajos
    y elimina acentos (diacríticos).
    """
    s = s.strip().replace(" ", "_").replace("/", "_").lower()
    s = unicodedata.normalize('NFKD', s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s


# Lista de tablas que se deben excluir (normalizadas)
EXCLUDED_TABLES = {
    "query_multiradio",
    "multiradio",
    "query_wega",
    "wega",
    "query_ypf",
    "ypf",
    "query_solarsol",
    "solarsol",
    "query_g2e",
    "g2e"
}

# Diccionario de esquemas esperados para cada tabla (usando nombres normalizados)
# Puedes ajustar o ampliar estos esquemas según tus necesidades.
TABLE_SCHEMAS = {
    "clientes": ["cliente_id", "nombre", "ciudad", "provincia", "telefono", "tipo_de_instalacion", "cuit", "id_mapa"],
    "comprobantes": ["comprobante_id", "presupuesto_id", "cliente_id", "vendedor_id", "fecha_emision", "monto_abonado",
                     "saldo_pendiente", "fecha_creacion", "metodo_pago", "observaciones"],
    "detalles_de_presupuestos": ["detalle_id", "presupuesto_id", "precio_id", "cantidad", "envio_unitario",
                                 "precio_en_pesos_manual", "precio_en_dolares", "iva", "margen_comercial",
                                 "descripcion_manual", "comentario"],
    "financiaciones": ["inactiva", "descripcion", "banco", "tarjetas", "dias_validos", "cuotas", "fecha_inicio",
                       "fecha_fin", "estado"],
    "kits_productos": ["kit_producto_id", "kit_id", "precio_id", "cantidad", "envio_unitario"],
    "kits": ["kit_id", "descripcion", "imagen", "folder_id"],
    "listas_de_precios": ["listadeprecio_id", "margen_comercial", "factor_extra", "nombre", "logo", "orden_prioridad"],
    "mapa_arg": ["id", "nombre", "provincia_nombre", "centroide_lon", "centroide_lat"],
    "presupuestos": ["presupuesto_id", "cliente_id", "proyecto_id", "fecha_de_creacion", "envio_total", "kit_id",
                     "link", "vendedor_id", "estado_ejecucion", "dispararproceso", "aplicar_descuento_efectivo"],
    "precios": ["precio_id", "descripcion", "precio_dolares", "iva", "disponibilidad", "margen_comercial",
                "listadeprecio_id", "precio_en_pesos", "margen_comercial_por_lista", "factor_extra_para_descuento"],
    # Otras tablas que importes pueden agregarse aquí...
}


def importar_csv_a_tabla(csv_path, table_name, db):
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        original_headers = next(reader, None)
        if not original_headers:
            return

        # Normalizamos los encabezados del CSV
        csv_headers = []
        for i, h in enumerate(original_headers):
            nh = normalize_string(h)
            if nh == "":
                nh = f"col{i + 1}"
            csv_headers.append(nh)

        # Normalizamos el nombre de la tabla
        normalized_table = normalize_string(table_name)

        # Si hay un esquema definido para esta tabla, lo usamos.
        if normalized_table in TABLE_SCHEMAS:
            expected_cols = TABLE_SCHEMAS[normalized_table]
        else:
            # Si no hay un esquema específico, usar los encabezados del CSV.
            expected_cols = csv_headers

        # Construir un mapeo de cada columna del CSV a su índice
        header_index = {col: idx for idx, col in enumerate(csv_headers)}

        # Para cada columna esperada, buscamos el índice en el CSV; si falta, usaremos None.
        # Esto genera la lista definitiva de columnas para el INSERT.
        insert_cols = expected_cols  # ya están normalizados
        placeholders = ",".join(["?" for _ in insert_cols])
        columns_sql = ",".join(insert_cols)

        insert_sql = f'INSERT INTO {normalized_table} ({columns_sql}) VALUES ({placeholders})'

        conn = db.connection
        cursor = conn.cursor()

        for row in reader:
            # Para cada columna esperada, buscamos el valor si existe; si no, None.
            new_row = []
            for col in expected_cols:
                if col in header_index:
                    new_row.append(row[header_index[col]])
                else:
                    new_row.append(None)
            try:
                cursor.execute(insert_sql, new_row)
            except Exception as e:
                print(f"Error al insertar en {normalized_table} con la fila {new_row}")
                raise e
        conn.commit()
        print(f"Importados datos de {csv_path} a la tabla {table_name}")


def main():
    db = DBManager()
    folder_csv = "Carpeta_CSV"
    archivos = os.listdir(folder_csv)
    for archivo in archivos:
        if archivo.endswith(".csv"):
            ruta = os.path.join(folder_csv, archivo)
            nombre_tabla = os.path.splitext(archivo)[0]
            normalized_table = normalize_string(nombre_tabla)
            if normalized_table in EXCLUDED_TABLES:
                print(f"Se omite la importación de {archivo} (tabla {nombre_tabla}).")
                continue
            try:
                importar_csv_a_tabla(ruta, nombre_tabla, db)
            except Exception as e:
                print(f"Error importando {archivo}: {e}")
    db.close_connection()


if __name__ == "__main__":
    main()
