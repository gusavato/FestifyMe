# FestifyMe


<center>
    <img src="./images/FestifyMe_logo.jpeg" alt="Alt text" width="300">
</center>


***

## Indice:
1.[📜 Descripción](#descripcion)\
2.[💡 Definición del problema](#problema)\
3.[⏳ Desarrollo](#desarrollo)\
4.[📈 Resultado](#resultado)\
5.[⏭️ Próximos Pasos](#next)\
5.[📁 Estructura](#Estructura)

## Descripción:<a name="descripcion"/>

FestifyMe es una app que te recomienda festivales de música en función de las 
playlist públicas de tu usario Spotify. Entre los casi 100 festivales que examina,
la app te recomendará 8 festivales por cada playlist. Además por cada festival 
propuesto, también te sugerirá 5 bandas que no se encuentran en tus playlist. En
este puedes ver su funcionamiento.

https://github.com/gusavato/FestifyMe/assets/69910815/8a36f4d6-7790-4f6b-9c13-6246909bfe12

## Definición del problema: <a name="problema"/>

En España tiene actualmente una oferta de festivales amplísima, haciendo que 
muchos de ellos coincidan en el tiempo. Esto hace que surja el problema de decidir 
a qué festival acudir.</br>
Aparte de esto, cada festival programa cada vez más artistas (El Primavera Sound 2023,
tiene programadas casi 200 bandas). Esto provaca que haya que optar por asistir a uno u
otro concierto, en su mayor parte de artistas que no conocemos. </br>
El problema que abordamos aquí es el de crear una herramienta, que dé una solución a estas
dos cuestiones:
- ¿A qué festival acudir?
- ¿A qué conciertos acudir de artistas que no conozco? 

## Desarrollo: <a name="desarrollo"/>

Para encontrar la solución al problema propuesto, partiremos de un 
[proyecto](https://github.com/gusavato/3_IRONHACK_ETL) previo,
donde se realizó la búsqueda de festivales programados en España en 2023.
En este proyecto se consolidó una base de datos donde se puede acceder a la información
de cada Festival, así como los datos que alberga Spotify de cada artista y de sus canciones.

Con esta información realizaremos los siguientes pasos:

1. Examinaremos las características del top 10 de canciones de todos los artistas que acuden
a los festivales. Con ello crearemos un vector que defina cada festival y cada banda, que se
usará para la generación de recomendaciones (Notebook [Artist_features](https://github.com/gusavato/FestifyMe/blob/main/src/jupyter/Artist_features.ipynb))

2. Crearemos un archivo [Spotipy_func.py](https://github.com/gusavato/FestifyMe/blob/main/src/Spotipy_func.py), donde defineremos distintas funciones, que nos permitiran obtener la 
información de Spotify de cada usario. El objetivo es analizar esta información, y crear 
distintos vectores para cada usuario, que se compararán con los de los fesitvales y grupos 
para obtener las recomendaciones.

3. En el archivo [DB_func.py](https://github.com/gusavato/FestifyMe/blob/main/src/DB_func.py), se definirán las funciones de carga y extracción de tablas a la base de datos

4. Se generarán recomendaciones con las funciones definidas en el archivo [Pred_func.py](https://github.com/gusavato/FestifyMe/blob/main/src/Pred_func.py). La metodología empleada es
comparar la [similitud de coseno](https://es.wikipedia.org/wiki/Similitud_coseno) de los distintos vectores implicados, y con ello generar una afinidad en %.

5. Por último, en el archivo [main.py](https://github.com/gusavato/FestifyMe/blob/main/src/main.py) se construye la estructura de la app desarrollada en [streamlit](https://docs.streamlit.io/)

## Resultado: <a name="resultado"/>

La app final con la que el usuario interactúa tiene el siguiente funcionamiento:

- Se introduce el usario de Spotify
- El programa genera una predicción de 8 festivales por cada playlist pública que
tenga el usario, y una predicción adicional donde se tienen en cuenta todas las playlists.
- Por cada festival se recomendarán 5 artistas que no están incluidos en ninguna de las playlists, y que tienen una alta afinidad con el usuario
- También se muestran las cabezas de cartel de cada festival, esta selección se basa en 
la popularidad de cada artista en Spotify.
- El usuario puede navegar por la aplicación selccionando distintos festivales y 
playlist. También puede hacer click en los distintos artistas, para que le redireccionen
a la página de Spotify del artista.