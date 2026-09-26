import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

print("=" * 55)
print("  LIMPIEZA DE DATOS DE PRUEBA")
print("=" * 55)

tablas_a_vaciar = [
    'ventas', 'detalle_ventas', 'clientes', 'proveedores',
    'articulos', 'productos', 'pedidos', 'pedidos_proveedor',
    'pedidos_detalle', 'historial_actividades',
]

print("\nVaciando tablas de negocio...")
for tabla in tablas_a_vaciar:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        antes = cursor.fetchone()[0]
        cursor.execute(f"DELETE FROM {tabla}")
        print(f"   OK - {tabla}: {antes} registros eliminados")
    except sqlite3.OperationalError as e:
        print(f"   AVISO - {tabla}: no existe ({e})")

print("\nEliminando usuarios que no sean 'admin'...")
cursor.execute("SELECT id, username FROM usuarios WHERE username != 'admin'")
for uid, uname in cursor.fetchall():
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (uid,))
    print(f"   OK - Eliminado: {uname} (ID {uid})")

print("\nReiniciando contadores...")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'")
if cursor.fetchone():
    for tabla in tablas_a_vaciar:
        try:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name = ?", (tabla,))
        except:
            pass
    print("   OK - Contadores reiniciados")

conn.commit()

print("\n" + "=" * 55)
print("  VERIFICACION FINAL")
print("=" * 55)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
for tabla in [t[0] for t in cursor.fetchall()]:
    cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
    print(f"   {tabla}: {cursor.fetchone()[0]} registros")

print("\nUsuarios restantes:")
cursor.execute("SELECT id, username FROM usuarios")
for fila in cursor.fetchall():
    print(f"   ID: {fila[0]} | Usuario: {fila[1]}")

conn.close()
print("\nBase de datos lista para el cliente.")