import socket

# Crear el socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8000))

print("Conectado al servidor.")

try:
    while True:
        try:
            # Leer el mensaje
            mensaje = client_socket.recv(1024).decode('utf-8').strip()

            # Si el servidor cierra la conexión, recv devolverá una cadena vacía
            if not mensaje:
                print("El servidor cerró la conexión.")
                break

            print(mensaje)

            # Condición para cerrar conexión si el mensaje contiene ciertas frases
            if mensaje in ["FIN", "Contraseña incorrecta. Acceso denegado.", "Usuario registrado con éxito. Por favor, inicie sesión nuevamente."]:
                break

            entrada = input()
            client_socket.send(entrada.encode('utf-8'))

        except ConnectionAbortedError:
            print("Error: La conexión fue cerrada por el servidor.")
            break

finally:
    client_socket.close()
    print("Conexión cerrada.")