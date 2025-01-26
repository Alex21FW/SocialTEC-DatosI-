# Hacer pip install passlib y bcrypt
import socket
import ssl
import threading
from passlib.hash import bcrypt
from Usuarios import cargar_usuarios, guardar_usuario  # Importar funciones del archivo usuarios.py
from amistades import GrafoAmistades

# Crear el grafo de amistades
amistades = GrafoAmistades()
lock = threading.Lock()  # Bloqueo para manejar operaciones en estructuras compartidas

# Crear el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8000))
server_socket.listen(5)  # Máximo 5 conexiones en cola

# Envolver el socket del servicor con SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
ssl_server_socket = context.wrap_socket(server_socket, server_side=True)

print("Servidor iniciado, esperando conexiones...")

def manejar_cliente(conexion_ssl, addr):
    #Maneja la interacción con un cliente en un hilo
    print("Nueva conexión desde:", addr)
    usuarios = cargar_usuarios()  # Cargar usuarios desde el archivo

    try:
        # Solicitar modo al cliente
        conexion_ssl.send(
            "Seleccione un modo:\n1. Inicio de sesión\n2. Registro".encode('utf-8')
        )
        modo = conexion.recv(1024).decode('utf-8').strip()

        if modo == "1":  # Modo de inicio de sesión
            conexion_ssl.send("Ingrese su usuario:".encode('utf-8'))
            usuario = conexion_ssl.recv(1024).decode('utf-8').strip()

            conexion_ssl.send("Ingrese su contraseña:".encode('utf-8'))
            contraseña = conexion_ssl.recv(1024).decode('utf-8').strip()

            # Verificar usuario y contraseña
            if usuario in usuarios and bcrypt.verify(contraseña, usuarios[usuario]):
                conexion_ssl.send(
                    "Inicio de sesión exitoso. Escribe 'salir' para desconectarte.\nOpciones disponibles:\n"
                    "1. Agregar amigo\n"
                    "2. Ver amigos\n"
                    "3. Ver quiénes te siguen\n"
                    "4. Comprobar ruta entre usuarios\n".encode('utf-8')
                )
                print(f"Usuario {usuario} inició sesión correctamente desde {addr}.")

                while True:
                    comando = conexion_ssl.recv(1024).decode('utf-8').strip()

                    if comando.lower() == "salir":
                        conexion_ssl.send("Desconexión exitosa. Hasta luego.".encode('utf-8'))
                        print(f"Usuario {usuario} se desconectó desde {addr}.")
                        break

                    elif comando == "1":  # Agregar amigo
                        conexion_ssl.send("Ingrese el nombre del amigo que desea agregar:".encode('utf-8'))
                        amigo = conexion_ssl.recv(1024).decode('utf-8').strip()

                        with lock:  # Bloquear acceso al grafo para operaciones seguras
                            if amigo == usuario:
                                conexion_ssl.send("No puedes agregarte como amigo.".encode('utf-8'))
                            elif amigo not in usuarios:
                                conexion_ssl.send("El usuario no existe en el sistema.".encode('utf-8'))
                            else:
                                amistades.agregar_amistad(usuario, amigo)
                                conexion_ssl.send(f"Amistad creada: {usuario} -> {amigo}".encode('utf-8'))

                    elif comando == "2":  # Ver amigos
                        with lock:
                            amigos = amistades.obtener_amistades(usuario)
                        conexion_ssl.send(
                            f"Tus amigos: {', '.join(amigos) if amigos else 'No tienes amigos :('}".encode('utf-8')
                        )

                    elif comando == "3":  # Ver quiénes te siguen
                        with lock:
                            seguidores = amistades.obtener_amigos(usuario)
                        conexion_ssl.send(
                            f"Usuarios que te siguen: {', '.join(seguidores) if seguidores else 'Nadie te sigue aún.'}".encode('utf-8')
                        )

                    elif comando == "4":  # Comprobar ruta
                        conexion_ssl.send("Ingrese el usuario inicial:".encode('utf-8'))
                        origen = conexion_ssl.recv(1024).decode('utf-8').strip()

                        conexion_ssl.send("Ingrese el usuario final:".encode('utf-8'))
                        destino = conexion_ssl.recv(1024).decode('utf-8').strip()

                        with lock:
                            if origen not in usuarios or destino not in usuarios:
                                conexion_ssl.send("Uno o ambos usuarios no existen en el sistema.".encode('utf-8'))
                            else:
                                ruta = amistades.ruta_entre_nodos(origen, destino)
                                if ruta:
                                    conexion_ssl.send(f"Ruta encontrada: {' -> '.join(ruta)}".encode('utf-8'))
                                else:
                                    conexion_ssl.send(f"No existe una ruta entre {origen} y {destino}".encode('utf-8'))
                    else:
                        conexion_ssl.send("Comando no válido. Intenta de nuevo.".encode('utf-8'))

            else:
                conexion_ssl.send("Credenciales incorrectas.".encode('utf-8'))
                print(f"Intento de inicio de sesión fallido desde {addr}.")

        elif modo == "2":  # Modo de registro
            conexion_ssl.send("Ingrese un nuevo usuario:".encode('utf-8'))
            nuevo_usuario = conexion_ssl.recv(1024).decode('utf-8').strip()

            conexion_ssl.send("Ingrese una nueva contraseña:".encode('utf-8'))
            nueva_contraseña = conexion_ssl.recv(1024).decode('utf-8').strip()

            with lock:
                if guardar_usuario(nuevo_usuario, nueva_contraseña):
                    amistades.agregar_usuario(nuevo_usuario)
                    conexion_ssl.send("Registro exitoso. Por favor, inicie sesión en el modo 1.".encode('utf-8'))
                else:
                    conexion_ssl.send("El usuario ya existe. Por favor, elija otro nombre.".encode('utf-8'))

        else:
            conexion_ssl.send("Modo no válido. Desconectando.".encode('utf-8'))

    except Exception as e:
        print(f"Error manejando la conexión con {addr}: {e}")

    finally:
        conexion_ssl.close()
        print(f"Conexión con {addr} cerrada.")


try:
    while True:
        conexion, addr = ssl_server_socket.accept()
        cliente_hilo = threading.Thread(target=manejar_cliente, args=(conexion, addr))
        cliente_hilo.start()  # Iniciar el hilo

except KeyboardInterrupt:
    print("\nServidor cerrado manualmente.")
finally:
    ssl_server_socket.close()
    print("Servidor cerrado.")