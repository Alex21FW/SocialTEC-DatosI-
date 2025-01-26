import socket
import ssl

# Crear el socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations("cert.pem") # Cargar el certificado del servidor
ssl_client_socket = context.wrap_socket(client_socket, server_hostname='localhost')

ssl_client_socket.connect(('localhost', 8000))

print("Conectado al servidor.")

try:
    while True:
        try:
            # Leer el mensaje
            mensaje = ssl_client_socket.recv(1024).decode('utf-8').strip()

            # Si el servidor cierra la conexión, recv devolverá una cadena vacía
            if not mensaje:
                print("El servidor cerró la conexión.")
                break

            print(mensaje)

            # Condición para cerrar conexión si el mensaje contiene ciertas frases
            if mensaje in ["Desconexión exitosa. Hasta luego.", "Contraseña incorrecta. Acceso denegado.", "Registro exitoso. Por favor, inicie sesión en el modo 1.", "Credenciales incorrectas."]:
                break

            entrada = input()
            ssl_client_socket.send(entrada.encode('utf-8'))

        except ConnectionAbortedError:
            print("Error: La conexión fue cerrada por el servidor.")
            break

finally:
    ssl_client_socket.close()
    print("Conexión cerrada.")