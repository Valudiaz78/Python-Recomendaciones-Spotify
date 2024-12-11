from collections import deque

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


