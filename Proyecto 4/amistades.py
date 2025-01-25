class GrafoAmistades:
    def __init__(self, archivo="conexiones.txt"):
        self.nodos = []  # Lista de nodos (usuarios)
        self.aristas = []  # Lista de aristas (amistades unidireccionales)
        self.archivo = archivo  # Archivo donde se guardan las conexiones
        self.cargar_conexiones()  # Cargar conexiones desde el archivo al iniciar

    def agregar_usuario(self, usuario):

        #Agrega un usuario al grafo si no existe.
        if usuario not in self.nodos:
            self.nodos.append(usuario)
            print(f"Usuario {usuario} agregado al grafo.")
            self.guardar_conexiones()  # Actualizar archivo

    def agregar_amistad(self, origen, destino):
        #Crea una relación de amistad unidireccional de 'origen' a 'destino'.

        if origen not in self.nodos:
            self.agregar_usuario(origen)

        if destino not in self.nodos:
            self.agregar_usuario(destino)

        if (origen, destino) not in self.aristas:
            self.aristas.append((origen, destino))
            print(f"Amistad creada: {origen} -> {destino}")
            self.guardar_conexiones()  # Actualizar archivo

        else:
            print(f"La amistad {origen} -> {destino} ya existe.")

    def obtener_amistades(self, usuario):
        #Devuelve las amistades salientes (amigos a los que sigue) del usuario.

        amigos = [destino for origen, destino in self.aristas if origen == usuario]
        return amigos

    def obtener_amigos(self, usuario):
        #Devuelve las personas que siguen al usuario

        seguidores = [origen for origen, destino in self.aristas if destino == usuario]
        return seguidores

    def mostrar_grafo(self):
        #Imprime todos los nodos y aristas del grafo.

        print("Nodos (usuarios):", ", ".join(self.nodos))
        print("Aristas (amistades):")

        for origen, destino in self.aristas:
            print(f"{origen} -> {destino}")

    def guardar_conexiones(self):
        #Guarda los nodos y aristas en el archivo de conexiones

        with open(self.archivo, "w") as file:
            # Guardar nodos
            file.write("# Nodos\n")
            for nodo in self.nodos:
                file.write(f"{nodo}\n")

            # Guardar aristas
            file.write("\n# Aristas\n")
            for origen, destino in self.aristas:
                file.write(f"{origen} -> {destino}\n")

        print("Conexiones guardadas en el archivo.")

    def cargar_conexiones(self):
        #Carga los nodos y aristas desde el archivo de conexiones

        try:
            with open(self.archivo, "r") as file:
                seccion = None

                for linea in file:
                    linea = linea.strip()
                    if not linea or linea.startswith("#"):
                        # Cambiar de sección según el encabezado
                        if linea == "# Nodos":
                            seccion = "nodos"
                        elif linea == "# Aristas":
                            seccion = "aristas"
                        continue

                    if seccion == "nodos":
                        self.nodos.append(linea)

                    elif seccion == "aristas":
                        origen, destino = linea.split(" -> ")
                        self.aristas.append((origen, destino))

            print("Conexiones cargadas desde el archivo.")
            
        except FileNotFoundError:
            print("Archivo de conexiones no encontrado. Se creará uno nuevo.")