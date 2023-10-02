# LAB01-HENRY
Puedes encontrar el deployment de la fast api aquí: <a href ="https://amaroroque.onrender.com/docs">FastAPI deployment

Puedes encontrar los dataset json aquí: <a href ="https://drive.google.com/drive/folders/1nC4rmtFUjJ-w2_q_ABLV9ypoH7HImY2T">Datasets JSON

Puedes encontrar los dataset csv aquí: <a href ="https://drive.google.com/drive/folders/1nC4rmtFUjJ-w2_q_ABLV9ypoH7HImY2T">Datasets csv

Puede encontrar el video aqui: <a href ="https://drive.google.com/drive/folders/1WXd3cUM_8dN_CGiFrw8hsUjEyiMyAQ7p"> Video

## **PROYECTO DE MACHINE LEARNING OPERATIONS (MLOps)**
**Descripción:** La plataforma multinacional de videojuegos ***STEAM***, requiere un sistema de recomendación con las siguientes métricas
- def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.
- def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
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

Consistió de un análisis descriptivo para ver que variables incluir en el sistema de recomendación, para más detalle dirígete a [EDA.ipynb](EDA.ipynb)
-   Aqui trabajamos con el archivo llamado [Archivo.csv](https://drive.google.com/drive/search?q=parent:1wLMybrjAryg2-qNfUOgdOpo3CqvqHNwK)
-   Hacemos un resumen estadístico con describe().

*Descripción de las variables cuantitativas*

|      | sentiment_analysis|  playtime_forever|         price|
|------|:------------------:|:------------------:|:--------------|
|count |       43402      |43402  |43402|
|mean  |          1.336|       2455.331|     14.620|
|std   |           0.761|       6243.369|     13.362|
|min   |           0|          0|      0|
|25%   |           1|         46|      9.990|
|50%   |           2|        229|     14.620|
|75%   |           2|       1005|    19.990|
|max   |           2|     141766|    771.710|

*Distribución de sentiment_analysis*

|sentiment_analysis||
|------------------|:-|
|2|    25536|
|1|    15194|
|0|     8456|
  
-   Luego nos centramos en la columna sentiment_analysis para ver la distribución de sus valores y se realiza un ploteo.
-   Hacemos los cambios respectivos a la columna precio, la cual tiene valores string, y se cambian por 0 y estos a su vez por la media.
-   Para las columnas genres y publisher, vizualizamos como están distribuidas, así tener presente que variable utilizar para el sitema de recomendación.
-   Se realiza una matriz de correlación, notanto que la correlación entre las variables cuantitativas es cercana a 0.
-   Luego guardamos el archivo con los cambios efectuados llamado [Archivo2](https://github.com/WilliamsAmaro/LAB01-HENRY/blob/main/Archivo2.csv)
-   Finalmente realizamos la función para el sistema de recomendación, utilizando la ***similitud del coseno****
-   Guardamos un dataset con las variables para el sistema de recomendación [aqui](https://github.com/WilliamsAmaro/LAB01-HENRY/blob/main/Archivo_SCoseno.csv)

**PASO 3: Creación del entorno de la FastAPI**

Dirígete al siguiente [enlace](https://github.com/WilliamsAmaro/LAB01-HENRY/blob/main/PasosFASTAPI.txt), donde se observa el paso a paso.

**PASO 4: Deployment de la API**

- Procedimos a subir los archivos a este repositorio: [main.py](https://github.com/WilliamsAmaro/LAB01-HENRY/blob/main/main.py), requirements.txt, configuración, y los datasets ([Archivo2](https://github.com/WilliamsAmaro/LAB01-HENRY/blob/main/Archivo2.csv) y [Archivo_SCoseno](https://github.com/WilliamsAmaro/LAB01-HENRY/blob/main/Archivo_SCoseno.csv))
- Asi queda el deployment:
![Imagen](https://github.com/WilliamsAmaro/LAB01-HENRY/blob/main/DeploymentAPI.png)


### AUTOR
[Williams Alexander Amaro Roque](linkedin.com/in/williams-alexander-amaro-roque-075b8421b/)

