import random
import logging
from collections import deque
from grafo import Grafo

logging.basicConfig(level=logging.DEBUG)


def bfs(grafo, origen, destino):
    
    # BFS para encontrar el camino más corto
    visitados = set()
    cola = deque([(origen, [])])
    
    while cola:
        actual, camino_actual = cola.popleft()
        
        if actual == destino:
            camino_actual.append(actual)
            return camino_actual
        
        if actual not in visitados:
            visitados.add(actual)
            for ady in grafo.obtener_adyacentes(actual):
                if ady not in visitados:
                    cola.append((ady, camino_actual + [actual]))
    
    return None

def pagerank(grafo, iteraciones=100, d=0.85):
    canciones = [v for v in grafo.obtener_vertices() if grafo.obtener_tipo_vertice(v) == "Cancion"]
    dict_pr = {cancion: 1 for cancion in canciones}
    for _ in range(iteraciones):
        for cancion in canciones:
            dict_pr[cancion] = ((1 - d)/len(canciones))+  d * sum([dict_pr[ady] / grafo.obtener_grado_vertice(ady) for ady in grafo.obtener_adyacentes(cancion) if ady in dict_pr])
    
    return dict_pr


def pagerank_personalizado(grafo, tipo, n, lista_origen):
    origen = random.choice(lista_origen)
    valor_original = 1
    pr_personalizado = {v: valor_original for v in grafo.obtener_vertices() if grafo.obtener_tipo_vertice(v) == tipo}
    
    for i in range(n*n):
        adyacentes = grafo.obtener_adyacentes(origen)
        if adyacentes == set():
            break
        ady = random.choice(list(adyacentes))
        valor_original *= (1 / grafo.obtener_grado_vertice(origen))
        pr_personalizado[ady] = valor_original
        origen = ady
    
    return pr_personalizado

def dfs(grafo, origen, camino, visitados, n):
    if len(camino) == n:
        if camino[0] in grafo.obtener_adyacentes(camino[-1]):
            return camino + [camino[0]]
        return None
    
    for adyacente in grafo.obtener_adyacentes(origen):
        if adyacente not in visitados:
            visitados.add(adyacente)
            camino.append(adyacente)
            resultado = dfs(grafo, adyacente, camino, visitados, n)
            if resultado:
                return resultado
            camino.pop()
            visitados.remove(adyacente)
    return None