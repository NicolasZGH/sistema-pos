import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(configuracion_sistema)")
columnas = cursor.fetchall()
print("COLUMNAS:")
for c in columnas:
    print(f"  {c}")

print("\nCONTENIDO:")
cursor.execute("SELECT * FROM configuracion_sistema")
for fila in cursor.fetchall():
    print(f"  {fila}")

conn.close()