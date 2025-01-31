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

    def eliminar_amistad(self, origen, destino):
        #Elimina una relacion de amistad (Elimina una arista)
        if (origen, destino) in self.aristas:
            self.aristas.remove((origen, destino))
            print(f"Amisnitad eliminada: {origen} -> {destino}")
            self.guardar_conexiones() #Actualizar el archivo
        
        else:
            print(f"La amistad {origen} -> {destino} no existe.")

    def obtener_amistades(self, usuario):
        #Devuelve las amistades salientes (amigos a los que sigue) del usuario.

        amigos = [destino for origen, destino in self.aristas if origen == usuario]
        return amigos

    def obtener_amigos(self, usuario):
        #Devuelve las personas que siguen al usuario

        seguidores = [origen for origen, destino in self.aristas if destino == usuario]
        return seguidores
    
    def ruta_entre_nodos(self, origen, destino):
        #Devuelve la ruta entre 'origen' y 'destino' si existe.
        if origen not in self.nodos or destino not in self.nodos:
            return None

        visitados = set()
        cola = [[origen]]   # Cola para BFS, cada elemento es una ruta completa

        while cola:
            ruta = cola.pop(0)
            nodo_actual = ruta[-1] #Ultimo nodo de la ruta actual

            if nodo_actual == destino:
                return ruta  

            if nodo_actual not in visitados:
                visitados.add(nodo_actual)
                for amigo in self.obtener_amistades(nodo_actual):
                    nueva_ruta = ruta.copy()  # Crear una copia de la ruta actual
                    nueva_ruta.append(amigo)  # Añadir el amigo a la nueva ruta
                    cola.append(nueva_ruta)  # Añadir la nueva ruta a la cola

        return None  # Si no se encuentra una ruta, devolver None
    
    def estadisticas_amistades(self):
        #Calcula estadisticas de los usuarios

        if not self.nodos:
            return "No hay usuarios en el sistema"
        
        #Crear diccionario para el conteo
        conteo_amistades = {usuario: len(self.obtener_amistades(usuario)) for usuario in self.nodos}

        max_amigos = max(conteo_amistades.values())
        min_amigos = min(conteo_amistades.values())

        usuarios_mas_amigos = [usuario for usuario, amigos in conteo_amistades.items() if amigos == max_amigos]
        usuarios_menos_amigos = [usuario for usuario, amigos in conteo_amistades.items() if amigos == min_amigos]

        total_amigos = sum(conteo_amistades.values())
        media_amigos = total_amigos / len(self.nodos) if self.nodos else 0

        resultado = (
            f"Estadisticas \n"
            f"Usuario con más amigos: {', '.join(usuarios_mas_amigos)} con ({max_amigos} amigos)\n"
            f"Usuario con menos amigos: {', '.join(usuarios_menos_amigos)} con ({min_amigos} amigos)\n"
            f"Media de amigos por usuario: {media_amigos:.2f}"
        )

        return resultado

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