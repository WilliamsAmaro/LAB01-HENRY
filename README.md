# LAB01-HENRY
Puedes encontrar el deployment de la fast api aquí: <a href ="https://amaroroque.onrender.com/docs">FastAPI deployment

Puedes encontrar los dataset json aquí: <a href ="https://drive.google.com/drive/folders/1nC4rmtFUjJ-w2_q_ABLV9ypoH7HImY2T">Datasets JSON

Puedes encontrar los dataset csv aquí: <a href ="https://drive.google.com/drive/folders/1nC4rmtFUjJ-w2_q_ABLV9ypoH7HImY2T">Datasets csv

Puede encontrar el video aqui: <a href ="https://drive.google.com/drive/folders/1WXd3cUM_8dN_CGiFrw8hsUjEyiMyAQ7p"> Video

## **PROYECTO DE MACHINE LEARNING OPERATIONS (MLOps)**
**Descripción:** LA plataforma multinacional de videojuegos ***STEAM***, requiere un sistema de recomendación con las siguientes métricas
- def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.
- def UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año.
- def UsersNotRecommend( año : int ): Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos).
- def sentiment_analysis( año : int ): Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
- def recomendacion_juego( id de producto ): Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

### **PASOS REALIZADOS**
**PASO 1: Realización del ETL**
En el archivo [ETL.ipynb](ETL.ipynb) se detalla el procedimiento realizado, a modo resumen se explica a continuación:
- Abrimos uno a uno los archivos json
- Se realizó un explode a la variable o columna anidada.
- Se procedió a realizar un desanidación con json_normalize
- Una vez visualizada todas las columnas, se hizo un reset al índice y realizado la conversión de los valores de cada columna según corresponda.
- Aquí se obtuvieron 3 archivos los cuales están ubicados aquí:

[Datasets](https://drive.google.com/drive/folders/1wLMybrjAryg2-qNfUOgdOpo3CqvqHNwK)

- Estos no se suben a este repositorio por restricciones de almacenamiento. Lo archivos que encontrarás son, uno llamado Reviews, Games, e Items, y el Archivo.csv donde está la unión de los 3 datasets.
  

**PASO 2: Realización del EDA**
Consistió de un análisis prescriptivo para ver que variables incluir en el sistema de recomendación, para más detalle dirígete a 
-   Aqui trabajamos con el archivo llamado [Archivo.csv](https://drive.google.com/drive/search?q=parent:1wLMybrjAryg2-qNfUOgdOpo3CqvqHNwK)
-   Hacemos un resumen estadístico con describe().
-   Luego nos centramos en la columna sentiment_analysis para ver la distribución de sus valores y se realiza un ploteo.
-   Hacemos los cambios respectivos a la columna precio, la cual tiene valores string, y se cambian por 0 y estos a su vez por la media.
-   Para las columnas genres y publisher, vizualizamos como están distribuidas, así tener presente que variable utilizar para el sitema de recomendación.
-   Se realiza una matriz de correlación, notanto que la correlación entre las variables cuantitativas es cercana a 0.
-   Luego guardamos el archivo con los cambios efectuados llamado Archivo2
-   Finalmente realizamos la función para el sistema de recomendación, utilizando la ***similitud del coseno****

