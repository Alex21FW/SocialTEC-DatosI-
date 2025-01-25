import socket

# Crear el socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8000))

print("Conectado al servidor.")

try:
    while True:
        #Leer el mensaje
        mensaje = client_socket.recv(1024).decode('utf-8')
        print (mensaje)

        if "Desconectado exitosa" in mensaje or "Acceso denegado" in mensaje:
            break

        entrada = input()
        client_socket.send(entrada.encode('utf-8'))

finally:
    client_socket.close()
    print("Conexion cerrada")