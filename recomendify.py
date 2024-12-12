 #!/usr/bin/env python

import sys
import csv
import grafo_aux
from grafo import Grafo


def cargar_datos(ruta_archivo):
    usuarios = set()
    canciones = set()
    playlists = set()
    usuario_canciones = {} #Almacena las canciones de cada usuario
    playlist_canciones = {} #Almacena las canciones de cada playlist
    usuario_playlists = {} #Almacena las playlists de cada usuario
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo, delimiter='\t')
        for linea in lector:
            usuario = linea['USER_ID']
            cancion = linea['TRACK_NAME'] + ' - ' + linea['ARTIST']
            playlist = linea['PLAYLIST_NAME']
            
            usuarios.add(usuario)
            canciones.add(cancion)
            playlists.add(playlist)

            if usuario not in usuario_canciones:
                usuario_canciones[usuario] = set()
            usuario_canciones[usuario].add(cancion) 

            if playlist not in playlist_canciones:
                playlist_canciones[playlist] = set()
            playlist_canciones[playlist].add(cancion)

            if playlist not in usuario_playlists:
                usuario_playlists[usuario] = set()
            usuario_playlists[usuario].add(playlist)

    return usuarios, canciones, usuario_canciones, playlist_canciones, usuario_playlists

def camino(grafo, origen, destino, usuario_canciones, playlist_canciones):
    if origen not in grafo.grafo or destino not in grafo.grafo:
        print("Tanto el origen como el destino deben ser canciones")
        return
    camino_encontrado = grafo_aux.bfs(grafo, origen, destino)
    if camino_encontrado:
        imprimir_camino(grafo, camino_encontrado, usuario_canciones, playlist_canciones)
    else:
        print("No se encontró recorrido")

def imprimir_camino(grafo, camino, playlist_canciones, usuario_playlists):
    resultado = []
    for i in range(len(camino)-1):
        if grafo.obtener_tipo_vertice(camino[i]) == "Cancion":
            cancion = camino[i]
            usuario = camino[i + 1]
            for playlist in grafo.obtener_peso_arista(cancion, usuario):
                if i == 0:
                    resultado.append(f"{cancion} ---> aparece en playlist ---> {playlist} ---> de ---> {usuario}")
                else:
                    resultado.append(f" ---> aparece en playlist ---> {playlist} ---> de ---> {usuario}")
        else:
            usuario = camino[i]
            cancion = camino[i + 1]
            for playlist in grafo.obtener_peso_arista(usuario, cancion):
                resultado.append(f" ---> tiene una playlist ---> {playlist} ---> donde aparece ---> {cancion}")
    print(" ".join(resultado))


def mas_importantes(grafo, n, pr):
    canciones_importantes = sorted(pr.items(), key=lambda item: item[1], reverse=True)
    top_canciones = [cancion for cancion, _ in canciones_importantes if cancion in grafo.obtener_vertices()][:n]
    print("; ".join(top_canciones))

def recomendacion(grafo, tipo, n, lista_origen):
    pr_personalizado = grafo_aux.pagerank_personalizado(grafo, tipo, n, lista_origen)
    recomendaciones = sorted(pr_personalizado.items(), key=lambda item: item[1], reverse=True)
    top_recomendaciones = [item for item, _ in recomendaciones if grafo.obtener_tipo_vertice(item) == "Cancion"][:n]
    print("; ".join(top_recomendaciones))


def ciclo(grafo, n, cancion):
    
    # Implementar la lógica para encontrar un ciclo de n canciones
    pass

def rango(n, cancion):
    # Implementar la lógica para encontrar todas las canciones en rango n
    pass

def construir_grafo(usuarios, canciones, usuario_canciones, playlist_canciones, usuario_playlists):
    grafo_bipartito = Grafo()

    for usuario in usuarios:
        grafo_bipartito.agregar_vertice(usuario, tipo="Usuario")
    for cancion in canciones:
        grafo_bipartito.agregar_vertice(cancion, tipo="Cancion")

    for usuario, canciones_usuario in usuario_canciones.items():
        for cancion in canciones_usuario:
            for playlist in usuario_playlists[usuario]:
                if cancion in playlist_canciones[playlist]:
                    grafo_bipartito.agregar_arista(usuario, cancion, playlist)
    
    return grafo_bipartito


def construir_grafo_canciones_usuario(canciones, usuario_canciones):
   #Relaciona canciones que le gustan al mismo usuario
    grafo = Grafo()
    for cancion in canciones:
        grafo.agregar_vertice(cancion)
    for usuario, canciones_usuario in usuario_canciones.items():
        for cancion1 in canciones_usuario:
            for cancion2 in canciones_usuario:
                if cancion1 != cancion2:
                    grafo.agregar_arista(cancion1, cancion2)
    return grafo

def main():
    if len(sys.argv) < 2:
        print("Ingrese en el formato: ./recomendify <ruta_archivo>")
        return
    
    ruta_archivo = sys.argv[1]
    usuarios, canciones, usuario_canciones, playlist_canciones, usuario_playlists = cargar_datos(ruta_archivo)
    grafo_bipartito = construir_grafo(usuarios, canciones, usuario_canciones, playlist_canciones, usuario_playlists)
    pr = grafo_aux.pagerank(grafo_bipartito)

    # Leer comandos
    for linea in sys.stdin:
        partes = linea.strip().split(' ')
        comando = partes[0]
        
        if comando == 'camino':
            origen, destino = ' '.join(partes[1:]).split(' >>>> ')
            camino(grafo_bipartito, origen, destino, playlist_canciones, usuario_playlists)
        elif comando == 'mas_importantes':
            n = int(partes[1])
            mas_importantes(grafo_bipartito, n, pr)
        elif comando == 'recomendacion':
            tipo = partes[1]
            n = int(partes[2])
            lista_origen = ' '.join(partes[3:]).split(' >>>> ')
            recomendacion(grafo_bipartito, tipo, n, lista_origen)
        elif comando == 'ciclo':
            n = int(partes[1])
            cancion = ' '.join(partes[2:])
            grafo = construir_grafo_canciones_usuario(canciones, usuario_canciones)
            ciclo(grafo, n, cancion)
        elif comando == 'rango':
            n = int(partes[1])
            cancion = ' '.join(partes[2:])
            rango(grafo_bipartito, n, cancion)
        else:
            print("Comando no reconocido")

if __name__ == "__main__":
    main()