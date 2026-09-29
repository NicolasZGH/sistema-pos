import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Ver estructura de ventas
cursor.execute("PRAGMA table_info(ventas)")
print("ESTRUCTURA DE LA TABLA 'ventas':")
print("=" * 60)
for col in cursor.fetchall():
    print(f"  {col}")

print()
print("ESTRUCTURA DE LA TABLA 'detalle_ventas':")
print("=" * 60)
cursor.execute("PRAGMA table_info(detalle_ventas)")
for col in cursor.fetchall():
    print(f"  {col}")

conn.close()