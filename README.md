# Recomendify

Se desarrolló en Python un sistema de recomendaciones de Spotify utilizando grafos.
### Correr el proyecto

```./recomendify [archivo.tsv]```

### Comandos

Una vez procesado el archivo tsv, se pueden correr los comandos

```camino [cancion] >>>> [cancion]```
Halla un camino conectando canciones guardadas en playlists de distintos usuarios
```mas_importantes n```
Muestra canciones mas importantes/centrales utilizando el algoritmo PageRank
```recomendacion ["usuario"/"canciones"] n [cancion 1 >>>> cancion 2 >>>> ...cancion n]```
Da recomendaciones tanto de usuarios como de canciones, basadas en canciones que ya sabemos que le gustan al usuario. Utiliza Pagerank personalizado
```ciclo [n] [cancion]```
Devuelve un ciclo de cierta cantidad de canciones empezando por la pedida
```rango [n] [cancion]``` 
Devuelve todas las canciones dentro de un rango respecto a una cancion