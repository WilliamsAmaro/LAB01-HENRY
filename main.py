from fastapi import FastAPI,  HTTPException
from fastapi import Query
from typing import Dict
import pandas as pd
import os
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# Obtengo la ruta absoluta del archivo CSV en base al directorio actual del script
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Archivo2.csv'))
# Cargo el archivo CSV utilizando la ruta absoluta
df_RIG = pd.read_csv(file_path)


app = FastAPI()

@app.get("/")
def presentación():
    return 'PROYECTO INDIVIDUAL 1 - Williams Amaro Roque'

#FUNCIONES
"""Función N°1: devuelve año con más horas jugadas para un genero """
# Defino la ruta para la función PlayTimeGenre
@app.get("/playtime_genre/")
def get_playtime_genre(genero: str = Query(..., description="Género para calcular las horas jugadas")):
    result = PlayTimeGenre(genero)
    return result

def PlayTimeGenre(genero: str):
    # Obtengo la ruta absoluta del archivo CSV en base al directorio actual del script
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Archivo2.csv'))
    # Cargo el archivo CSV utilizando la ruta absoluta
    df_RIG = pd.read_csv(file_path)
    # Filtro el DataFrame por el género especificado
    filtered_df = df_RIG[df_RIG['genres'].str.contains(genero, case=False, na=False)]

    # Agrupo por año de lanzamiento y calculo la suma de horas jugadas para cada año
    grouped = filtered_df.groupby('year_game')['playtime_forever'].sum()

    # Par encontrar el año con la suma máxima de horas jugadas
    year_max_playtime = grouped.idxmax()

    # Creo el resultado
    result = {"Año de lanzamiento con más horas jugadas para Género " + genero: year_max_playtime}

    return result

@app.get("/user_for_genre/")
def get_user_for_genre(genero: str = Query(..., description="Género para buscar el usuario con más horas jugadas")):
    result = UserForGenre(genero)
    return result

def UserForGenre(genero: str):
    # Obtengo la ruta absoluta del archivo CSV en base al directorio actual del script
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Archivo2.csv'))
    # Cargo el archivo CSV utilizando la ruta absoluta
    df_RIG = pd.read_csv(file_path)    
    
    # Filtro el DataFrame por el género especificado
    filtered_df = df_RIG[df_RIG['genres'].str.contains(genero, case=False, na=False)]

    # Agrupo por usuario y calculo la suma de horas jugadas para cada usuario
    grouped_users = filtered_df.groupby('user_id')['playtime_forever'].sum()

    # el usuario con la suma máxima de horas jugadas
    user_max_playtime = grouped_users.idxmax()

    # Filtro las filas para el usuario encontrado
    user_df = filtered_df[filtered_df['user_id'] == user_max_playtime]

    # Agrupo por año de lanzamiento y calculo la suma de horas jugadas para cada año
    grouped_years = user_df.groupby('year_game')['playtime_forever'].sum()

    # Creo una lista de diccionarios con el año y las horas jugadas acumuladas para cada año
    hours_by_year = [{"Año": year, "Horas": hours} for year, hours in grouped_years.items()]

    # Creo el resultado en el formato deseado
    result = {"Usuario con más horas jugadas para Género " + genero: user_max_playtime, "Horas jugadas": hours_by_year}

    return result

# Defino la ruta para la función UsersRecommend
@app.get("/users_recommend/")
def get_users_recommend(año: int = Query(..., description="Año para buscar los juegos recomendados")):
    result = UsersRecommend(año)
    return result

def UsersRecommend(año: int): 
    # Obtengo la ruta absoluta del archivo CSV en base al directorio actual del script
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Archivo2.csv'))
    # Cargo el archivo CSV utilizando la ruta absoluta
    df_RIG = pd.read_csv(file_path)    
    
    # Filtro el DataFrame por el año especificado, recommend=True y comentarios positivos/neutrales
    filtered_df = df_RIG[(df_RIG['year_review'] == año) & (df_RIG['recommend'] == True) & (df_RIG['sentiment_analysis'] > 0)]

    # Agrupo las filas por el nombre del juego y contar las recomendaciones
    game_recommendations = filtered_df.groupby('item_name')['recommend'].count().reset_index()

    # Ordeno los juegos por el número de recomendaciones en orden descendente
    top_games = game_recommendations.sort_values(by='recommend', ascending=False)

    # Selecciono los 3 juegos principales
    top_3_games = top_games.head(3)

    # resultado
    result = [{"Puesto {}: {}".format(i + 1, juego)} for i, juego in enumerate(top_3_games['item_name'])]

    return result


# Defino la ruta para la función UsersNotRecommend
@app.get("/users_not_recommend/")
def get_users_not_recommend(año: int = Query(..., description="Año para buscar los juegos menos recomendados")):
    result = UsersNotRecommend(año)
    return result

def UsersNotRecommend(año: int):
    # Obtengo la ruta absoluta del archivo CSV en base al directorio actual del script
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Archivo2.csv'))
    # Cargo el archivo CSV utilizando la ruta absoluta
    df_RIG = pd.read_csv(file_path)
    
    # Filtro el DataFrame por el año especificado y comentarios negativos
    filtered_df = df_RIG[(df_RIG['year_review'] == año) & (df_RIG['sentiment_analysis'] == 0)]

    # Verifico si hay datos disponibles
    if filtered_df.empty:
        return "No hay datos disponibles para ese año y comentarios negativos."

    # Agrupo las filas por el nombre del juego y cuento las no recomendaciones
    game_not_recommendations = filtered_df.groupby('item_name')['sentiment_analysis'].count().reset_index()

    # Ordeno los juegos por el número de comentarios negativos en orden ascendente
    bottom_games = game_not_recommendations.sort_values(by='sentiment_analysis', ascending=True)

    # Selecciono los 3 juegos principales (los menos recomendados)
    top_3_bottom_games = bottom_games.head(3)

    # Resultado
    result = [{"Puesto {}: {}".format(i + 1, juego)} for i, juego in enumerate(top_3_bottom_games['item_name'])]

    return result

@app.get("/sentiment_analysis/")
def get_sentiment_analysis(año: int = Query(..., description="Año para analizar el sentimiento de las reseñas")) -> Dict[str, int]:
    result = sentiment_analysis(año)
    return result

def sentiment_analysis(año: int) -> Dict[str, int]:  
    # Filtro el DataFrame por el año especificado
    filtered_df = df_RIG[df_RIG['year_review'] == año]
    # la cantidad de valores 0, 1 y 2 en la columna 'sentiment_analysis'
    negative_count = (filtered_df['sentiment_analysis'] == 0).sum()
    neutral_count = (filtered_df['sentiment_analysis'] == 1).sum()
    positive_count = (filtered_df['sentiment_analysis'] == 2).sum()
    # Resultado
    result = {"Negative": negative_count, "Neutral": neutral_count, "Positive": positive_count}
    return result

# Cargo el archivo CSV
# Obtengo la ruta absoluta del archivo CSV en base al directorio actual del script
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Archivo_SCoseno.csv'))
# Cargo el archivo CSV utilizando la ruta absoluta
features = pd.read_csv(file_path)

@app.get("/recomendar/{item_id}", response_model=List[str])
def obtener_recomendaciones(item_id: int, num_recomendaciones: int = 5):
    try:
        result = recomendacion_juego(item_id, num_recomendaciones)
        return result
    except HTTPException as e:
        raise e
#Funcion
def recomendacion_juego(item_id: int, num_recomendaciones: int = 5):
    #Filtro el juego por su id
    juego_seleccionado = features[features['item_id'] == item_id]
    #verifico si el juego existe
    if juego_seleccionado.empty:
        raise HTTPException(status_code=404, detail="El item_id no se encuentra en los datos")
    #calculo la similitud del coseno
    cosine_sim = cosine_similarity(juego_seleccionado.iloc[:, :-2], features.iloc[:, :-2])
    sim_scores = list(enumerate(cosine_sim[0]))
    # Ordenando los juegos por similitud en orden descendente
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    #Selecciono los juegos mas similares
    top_similar_games = sim_scores[1:(num_recomendaciones + 1)]
    #obtengo los nombres de los juegos recomendados
    recomendaciones = [features.iloc[i[0]]['item_name'] for i in top_similar_games]
    return recomendaciones
