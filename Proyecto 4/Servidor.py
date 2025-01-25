# Hacer pip install passlib y bcrypt
import socket
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
        print(f"El usuario {usuario} ya esta registrado")
        return
    
    with open(USUARIOS_FILE, "a") as file:
        password_hash = bcrypt.hash(contraseña)
        file.write(f"\n{usuario}|{password_hash}")
    print(f"Usuario {usuario} registrado con éxito.")

# Crear el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8000))
server_socket.listen(5)  # Máximo 5 conexiones en cola

print("Servidor iniciado, esperando conexiones...")

try:
    while True:
        conexion, addr = server_socket.accept()
        print("Nueva conexión desde:", addr)

        usuarios = cargar_usuarios()  # Cargar usuarios desde el archivo

        try:
            # Solicitar nombre de usuario
            conexion.send("Ingrese su nombre de usuario:".encode('utf-8'))
            usuario = conexion.recv(1024).decode('utf-8')

            # Verificar si el usuario existe
            if usuario not in usuarios:
                conexion.send("Usuario no encontrado. ¿Desea registrarse? (si/no):".encode('utf-8'))
                respuesta = conexion.recv(1024).decode('utf-8').strip().lower()
                if respuesta == "si":
                    conexion.send("Ingrese una nueva contraseña:".encode('utf-8'))
                    nueva_contraseña = conexion.recv(1024).decode('utf-8')
                    guardar_usuario(usuario, nueva_contraseña)
                    conexion.send("Usuario registrado con éxito. Por favor, inicie sesión nuevamente.".encode('utf-8'))
                else:
                    conexion.send("Desconexión por usuario no registrado.".encode('utf-8'))
                conexion.close()  # Cerrar la conexión solo después de enviar el mensaje
                continue  # Volver a aceptar una nueva conexión

            # Solicitar contraseña
            conexion.send("Ingrese su contraseña:".encode('utf-8'))
            contraseña = conexion.recv(1024).decode('utf-8')

            # Verificar la contraseña
            if bcrypt.verify(contraseña, usuarios[usuario]):
                conexion.send("Inicio de sesión exitoso. Escribe 'salir' para desconectarte. Bienvenido.".encode('utf-8'))
                print(f"Usuario {usuario} inició sesión correctamente desde {addr}.")

                while True:
                    comando = conexion.recv(1024).decode('utf-8').strip()

                    if comando.lower() == "salir":
                        conexion.send("FIN".encode('utf-8'))
                        print(f"Usuario {usuario} se desconectó desde {addr}")
                        break

                    respuesta = f"Comando recibido: {comando}"
                    conexion.send(respuesta.encode('utf-8'))

            else:
                conexion.send("Contraseña incorrecta. Acceso denegado.".encode('utf-8'))
                print(f"Intento fallido de inicio de sesión de {usuario} desde {addr}.")

        except Exception as e:
            print(f"Error manejando la conexión con {addr}: {e}")

        finally:
            # Cerrar la conexión con el cliente
            conexion.close()
            print(f"Conexión con {addr} cerrada.")

except KeyboardInterrupt:
    print("\nServidor cerrado manualmente.")
finally:
    # Asegurar el cierre del socket del servidor
    server_socket.close()
    print("Servidor cerrado.")