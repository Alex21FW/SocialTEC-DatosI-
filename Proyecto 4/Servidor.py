# Hacer pip install passlib y bcrypt
import socket
from passlib.hash import bcrypt
from Usuarios import cargar_usuarios, guardar_usuario  # Importar funciones del archivo usuarios.py

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
            # Solicitar modo al cliente
            conexion.send("Seleccione un modo: 1 para inicio de sesión, 2 para registro:".encode('utf-8'))
            modo = conexion.recv(1024).decode('utf-8').strip()

            if modo == "1":  # Modo de inicio de sesión
                conexion.send("Ingrese su usuario:".encode('utf-8'))
                usuario = conexion.recv(1024).decode('utf-8').strip()

                conexion.send("Ingrese su contraseña:".encode('utf-8'))
                contraseña = conexion.recv(1024).decode('utf-8').strip()

                # Verificar usuario y contraseña
                if usuario in usuarios and bcrypt.verify(contraseña, usuarios[usuario]):
                    conexion.send("Inicio de sesión exitoso. Escribe 'salir' para desconectarte.".encode('utf-8'))
                    print(f"Usuario {usuario} inició sesión correctamente desde {addr}.")

                    while True:
                        comando = conexion.recv(1024).decode('utf-8').strip()

                        if comando.lower() == "salir":
                            conexion.send("FIN".encode('utf-8'))
                            print(f"Usuario {usuario} se desconectó desde {addr}.")
                            break

                        respuesta = f"Comando recibido: {comando}"
                        conexion.send(respuesta.encode('utf-8'))
                else:
                    conexion.send("Credenciales incorrectas.".encode('utf-8'))
                    print(f"Intento de inicio de sesión fallido desde {addr}.")

            elif modo == "2":  # Modo de registro
                conexion.send("Ingrese un nuevo usuario:".encode('utf-8'))
                nuevo_usuario = conexion.recv(1024).decode('utf-8').strip()

                conexion.send("Ingrese una nueva contraseña:".encode('utf-8'))
                nueva_contraseña = conexion.recv(1024).decode('utf-8').strip()

                if guardar_usuario(nuevo_usuario, nueva_contraseña):
                    conexion.send("Registro exitoso. Por favor, inicie sesión en el modo 1.".encode('utf-8'))
                else:
                    conexion.send("El usuario ya existe. Por favor, elija otro nombre.".encode('utf-8'))

            else:
                conexion.send("Modo no válido. Desconectando.".encode('utf-8'))

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