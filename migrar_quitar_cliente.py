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

print("\nMigrando tabla 'ventas'...")

# 3. Desactivar foreign keys temporalmente
cursor.execute("PRAGMA foreign_keys=OFF")

# 4. Renombrar la tabla actual
cursor.execute("ALTER TABLE ventas RENAME TO ventas_viejo")
print("  - Tabla 'ventas' renombrada a 'ventas_viejo'")

# 5. Crear la nueva tabla SIN la columna 'cliente'
cursor.execute("""
    CREATE TABLE ventas (
        factura INTEGER,
        articulo TEXT,
        precio REAL,
        cantidad INTEGER,
        total REAL,
        fecha TEXT,
        hora TEXT,
        costo REAL
    )
""")
print("  - Nueva tabla 'ventas' creada (sin columna cliente)")

# 6. Copiar los datos (excluyendo cliente)
cursor.execute("""
    INSERT INTO ventas (factura, articulo, precio, cantidad, total, fecha, hora, costo)
    SELECT factura, articulo, precio, cantidad, total, fecha, hora, costo
    FROM ventas_viejo
""")
filas = cursor.rowcount
print(f"  - {filas} filas copiadas a la nueva tabla")

# 7. Borrar la tabla vieja
cursor.execute("DROP TABLE ventas_viejo")
print("  - Tabla 'ventas_viejo' eliminada")

# 8. Reactivar foreign keys
cursor.execute("PRAGMA foreign_keys=ON")

# 9. Commit
conn.commit()

# 10. Verificación
cursor.execute("PRAGMA table_info(ventas)")
print("\nNueva estructura de 'ventas':")
for col in cursor.fetchall():
    print(f"  {col}")

cursor.execute("SELECT COUNT(*) FROM ventas")
print(f"\nTotal de ventas conservadas: {cursor.fetchone()[0]}")

conn.close()
print("\nMigracion completada exitosamente.")