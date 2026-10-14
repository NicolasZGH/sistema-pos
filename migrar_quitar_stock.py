import sqlite3
import shutil
from datetime import datetime

# 1. Respaldo automático
fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
respaldo = f"database_respaldo_{fecha}.db"
shutil.copy("database.db", respaldo)
print(f"Respaldo creado: {respaldo}")

# 2. Conectar
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# 3. Desactivar foreign keys temporalmente
cursor.execute("PRAGMA foreign_keys=OFF")


def columnas(tabla):
    """Devuelve los nombres de columna de una tabla (o lista vacía si no existe)."""
    return [col[1] for col in cursor.execute(f"PRAGMA table_info({tabla})").fetchall()]


def migrar_tabla(tabla, columnas_restantes, columnas_select, definicion):
    """Recrea una tabla sin la columna 'stock' conservando los datos."""
    if tabla not in [t[0] for t in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
        print(f"\nTabla '{tabla}' no existe, se omite.")
        return

    cols_actuales = columnas(tabla)
    if "stock" not in cols_actuales:
        print(f"\nTabla '{tabla}' ya no tiene la columna 'stock', se omite.")
        return

    print(f"\nMigrando tabla '{tabla}'...")

    # Renombrar la tabla actual
    cursor.execute(f"ALTER TABLE {tabla} RENAME TO {tabla}_viejo")
    print(f"  - Tabla '{tabla}' renombrada a '{tabla}_viejo'")

    # Crear la nueva tabla SIN la columna 'stock'
    cursor.execute(f"CREATE TABLE {tabla} ({definicion})")
    print(f"  - Nueva tabla '{tabla}' creada (sin columna stock)")

    # Copiar los datos (excluyendo stock)
    cursor.execute(
        f"INSERT INTO {tabla} ({', '.join(columnas_restantes)}) "
        f"SELECT {', '.join(columnas_select)} FROM {tabla}_viejo"
    )
    filas = cursor.rowcount
    print(f"  - {filas} filas copiadas a la nueva tabla")

    # Borrar la tabla vieja
    cursor.execute(f"DROP TABLE {tabla}_viejo")
    print(f"  - Tabla '{tabla}_viejo' eliminada")


# 4. Migrar articulos
migrar_tabla(
    tabla="articulos",
    columnas_restantes=["id", "codigo", "articulo", "precio", "costo", "estado", "imagen_path"],
    columnas_select=["id", "codigo", "articulo", "precio", "costo", "estado", "imagen_path"],
    definicion="""
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE,
        articulo TEXT NOT NULL,
        precio REAL NOT NULL,
        costo REAL NOT NULL,
        estado TEXT NOT NULL,
        imagen_path TEXT
    """,
)

# 5. Migrar productos
migrar_tabla(
    tabla="productos",
    columnas_restantes=["id", "codigo", "nombre", "precio", "costo", "estado", "imagen_path"],
    columnas_select=["id", "codigo", "nombre", "precio", "costo", "estado", "imagen_path"],
    definicion="""
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        costo REAL NOT NULL,
        estado TEXT DEFAULT 'Activo',
        imagen_path TEXT
    """,
)

# 6. Reactivar foreign keys
cursor.execute("PRAGMA foreign_keys=ON")

# 7. Commit
conn.commit()

# 8. Verificación
for tabla in ("articulos", "productos"):
    if tabla in [t[0] for t in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
        print(f"\nNueva estructura de '{tabla}':")
        for col in cursor.execute(f"PRAGMA table_info({tabla})").fetchall():
            print(f"  {col}")
        print(f"Total de filas en '{tabla}': {cursor.execute(f'SELECT COUNT(*) FROM {tabla}').fetchone()[0]}")

conn.close()
print("\nMigracion completada exitosamente.")
