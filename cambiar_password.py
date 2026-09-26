import sqlite3
import hashlib

usuario = "admin"
nueva_password = input("Nueva contrasena para 'admin': ").strip()

if not nueva_password:
    print("Contrasena vacia. Cancelado.")
    exit()

if len(nueva_password) < 6:
    print("La contrasena debe tener al menos 6 caracteres.")
    exit()

password_hash = hashlib.sha256(nueva_password.encode()).hexdigest()

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("UPDATE usuarios SET password = ? WHERE username = ?", (password_hash, usuario))
conn.commit()
conn.close()

print(f"Contrasena actualizada para '{usuario}'.")