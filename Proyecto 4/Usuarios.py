from passlib.hash import bcrypt

# Archivo donde se almacenan los usuarios y contraseñas encriptadas
USUARIOS_FILE = "usuarios.txt"

# Función para cargar usuarios desde el archivo
def cargar_usuarios():
    usuarios = {}
    try:
        with open(USUARIOS_FILE, "r") as file:
            for linea in file:
                usuario, password_hash = linea.strip().split("|")
                usuarios[usuario] = password_hash
    except FileNotFoundError:
        print("Archivo de usuarios no encontrado, se creará uno nuevo.")
    return usuarios

# Función para guardar un nuevo usuario en el archivo
def guardar_usuario(usuario, contraseña):
    usuarios = cargar_usuarios()

    if usuario in usuarios:
        print(f"El usuario {usuario} ya está registrado.")
        return False
    
    with open(USUARIOS_FILE, "a") as file:
        password_hash = bcrypt.hash(contraseña)
        file.write(f"\n{usuario}|{password_hash}")
    print(f"Usuario {usuario} registrado con éxito.")
    return True