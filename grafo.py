class Grafo:

    def __init__(self):
        self.grafo = {}
        self.grado_vertices = {}
        self.tipo = {}  # "Cancion" o "Usuario"

    def agregar_vertice(self, vertice, tipo=None):
        if vertice not in self.grafo:
            self.grafo[vertice] = {}
            self.grado_vertices[vertice] = 0
            if tipo:
                self.tipo[vertice] = tipo

    def agregar_arista(self, vertice1, vertice2, playlist=None):
        self.grafo[vertice1] = self.grafo.get(vertice1, {})
        self.grafo[vertice2] = self.grafo.get(vertice2, {})
        self.grafo[vertice1][vertice2] = self.grafo[vertice1].get(vertice2, set())
        self.grafo[vertice2][vertice1] = self.grafo[vertice2].get(vertice1, set())
        self.grafo[vertice1][vertice2].add(playlist) # Las playlists actuan como pesos
        self.grafo[vertice2][vertice1].add(playlist)

        self.grado_vertices[vertice1] = self.grado_vertices.get(vertice1, 0) + 1
        self.grado_vertices[vertice2] = self.grado_vertices.get(vertice2, 0) + 1

    def obtener_vertices(self):
        return self.grafo.keys()
    
    def pertenece(self, vertice):
        return vertice in self.grafo
    
    def estan_unidos(self, vertice1, vertice2):
        return vertice2 in self.grafo[vertice1]
    
    def obtener_adyacentes(self, vertice):
        if vertice in self.grafo:
            return self.grafo[vertice]
        return {}
    
    def obtener_peso_arista(self, vertice1, vertice2):
        if vertice1 in self.grafo and vertice2 in self.grafo[vertice1]:
            return self.grafo[vertice1][vertice2]
        return 0
    
    def obtener_tipo_vertice(self, vertice):
        if vertice in self.grafo:
            return self.tipo[vertice]
        return None 
    
    def obtener_grado_vertice(self, vertice):
        if vertice in self.grafo:
            return self.grado_vertices[vertice]
        return None

    def __str__(self):
        return str(self.grafo)