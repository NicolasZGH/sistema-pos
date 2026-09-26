import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Listar todas las tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tablas = [t[0] for t in cursor.fetchall()]

print("=" * 50)
print("TABLAS Y CANTIDAD DE REGISTROS")
print("=" * 50)

for tabla in tablas:
    cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
    cantidad = cursor.fetchone()[0]
    print(f"{tabla}: {cantidad} registros")

print()
print("=" * 50)
print("USUARIOS REGISTRADOS")
print("=" * 50)
try:
    cursor.execute("SELECT id, username FROM usuarios")
    for fila in cursor.fetchall():
        print(f"  ID: {fila[0]} | Usuario: {fila[1]}")
except Exception as e:
    print(f"Error: {e}")

conn.close()