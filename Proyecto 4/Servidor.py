#Hacer pip install passlib y bcrypt
import socket
from passlib.hash import bcrypt

# Base de datos simulada de usuarios (nombre de usuario y contraseña)
usuarios = {
    "usuario1": bcrypt.hash("contraseña123"),
    "admin": bcrypt.hash("admin123"),
}

# Crear el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8000))
server_socket.listen(5)  # Máximo 5 conexiones en cola

print("Servidor iniciado, esperando conexiones...")

try:
    while True:
        conexion, addr = server_socket.accept()
        print("Nueva conexión desde:", addr)

        try:
            # Solicitar nombre de usuario
            conexion.send("Ingrese su nombre de usuario:".encode('utf-8'))
            usuario = conexion.recv(1024).decode('utf-8')

            # Verificar si el usuario existe
            if usuario not in usuarios:
                conexion.send("Usuario no encontrado. Desconectando...".encode('utf-8'))
                conexion.close()
                print(f"Intento de inicio de sesión fallido desde {addr}. Usuario no encontrado.")
                continue

            # Solicitar contraseña
            conexion.send("Ingrese su contraseña:".encode('utf-8'))
            contraseña = conexion.recv(1024).decode('utf-8')

            # Verificar la contraseña
            if bcrypt.verify(contraseña, usuarios[usuario]):
                conexion.send("Inicio de sesión exitoso. Escribe 'salir' para desconectarte Bienvenido.".encode('utf-8'))
                print(f"Usuario {usuario} inició sesión correctamente desde {addr}.")
                

                while True:
                    comando = conexion.recv(1024).decode('utf-8').strip()

                    if comando.lower() == "salir":
                        conexion.send("FIN".encode('utf-8'))
                        print(f"Usuario {usuario} se desconecto desde {addr}")
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