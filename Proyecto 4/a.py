from passlib.hash import bcrypt

# Define la nueva contraseña
nueva_contraseña = "admin123"

# Generar el hash
nuevo_hash = bcrypt.hash(nueva_contraseña)

print(f"Hash para la nueva contraseña: {nuevo_hash}")