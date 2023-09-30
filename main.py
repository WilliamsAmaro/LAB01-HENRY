from fastapi import FastAPI,  HTTPException
from fastapi import Query
from typing import Dict
import pandas as pd
import os
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# Obtener la ruta absoluta del archivo CSV en base al directorio actual del script
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Archivo2.csv'))
# Cargar el archivo CSV utilizando la ruta absoluta
df_RIG = pd.read_csv(file_path)


app = FastAPI()

@app.get("/")
def presentación():
    return 'PROYECTO INDIVIDUAL 1 - Williams Amaro Roque'

#FUNCIONES
"""Función N°1: devuelve año con más horas jugadas para un genero """
# Definir la ruta para la función PlayTimeGenre
@app.get("/playtime_genre/")
def get_playtime_genre(genero: str = Query(..., description="Género para calcular las horas jugadas")):
    result = PlayTimeGenre(genero)
    return result

def PlayTimeGenre(genero: str):
    # Obtener la ruta absoluta del archivo CSV en base al directorio actual del script
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Archivo2.csv'))
    # Cargar el archivo CSV utilizando la ruta absoluta
    df_RIG = pd.read_csv(file_path)
    # Filtrar el DataFrame por el género especificado
    filtered_df = df_RIG[df_RIG['genres'].str.contains(genero, case=False, na=False)]

    # Agrupar por año de lanzamiento y calcular la suma de horas jugadas para cada año
    grouped = filtered_df.groupby('year_game')['playtime_forever'].sum()

    # Encontrar el año con la suma máxima de horas jugadas
    year_max_playtime = grouped.idxmax()

    # Crear el resultado en el formato deseado
    result = {"Año de lanzamiento con más horas jugadas para Género " + genero: year_max_playtime}

    return result

@app.get("/user_for_genre/")
def get_user_for_genre(genero: str = Query(..., description="Género para buscar el usuario con más horas jugadas")):
    result = UserForGenre(genero)
    return result

def UserForGenre(genero: str):
    # Obtener la ruta absoluta del archivo CSV en base al directorio actual del script
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Archivo2.csv'))
    # Cargar el archivo CSV utilizando la ruta absoluta
    df_RIG = pd.read_csv(file_path)    
    
    # Filtrar el DataFrame por el género especificado
    filtered_df = df_RIG[df_RIG['genres'].str.contains(genero, case=False, na=False)]

    # Agrupar por usuario y calcular la suma de horas jugadas para cada usuario
    grouped_users = filtered_df.groupby('user_id')['playtime_forever'].sum()

    # Encontrar el usuario con la suma máxima de horas jugadas
    user_max_playtime = grouped_users.idxmax()

    # Filtrar las filas para el usuario encontrado
    user_df = filtered_df[filtered_df['user_id'] == user_max_playtime]

    # Agrupar por año de lanzamiento y calcular la suma de horas jugadas para cada año
    grouped_years = user_df.groupby('year_game')['playtime_forever'].sum()

    # Crear una lista de diccionarios con el año y las horas jugadas acumuladas para cada año
    hours_by_year = [{"Año": year, "Horas": hours} for year, hours in grouped_years.items()]

    # Crear el resultado en el formato deseado
    result = {"Usuario con más horas jugadas para Género " + genero: user_max_playtime, "Horas jugadas": hours_by_year}

    return result

# Definir la ruta para la función UsersRecommend
@app.get("/users_recommend/")
def get_users_recommend(año: int = Query(..., description="Año para buscar los juegos recomendados")):
    result = UsersRecommend(año)
    return result

def UsersRecommend(año: int): 
    # Obtener la ruta absoluta del archivo CSV en base al directorio actual del script
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Archivo2.csv'))
    # Cargar el archivo CSV utilizando la ruta absoluta
    df_RIG = pd.read_csv(file_path)    
    
    # Filtrar el DataFrame por el año especificado, recommend=True y comentarios positivos/neutrales
    filtered_df = df_RIG[(df_RIG['year_review'] == año) & (df_RIG['recommend'] == True) & (df_RIG['sentiment_analysis'] > 0)]

    # Agrupar las filas por el nombre del juego y contar las recomendaciones
    game_recommendations = filtered_df.groupby('item_name')['recommend'].count().reset_index()

    # Ordenar los juegos por el número de recomendaciones en orden descendente
    top_games = game_recommendations.sort_values(by='recommend', ascending=False)

    # Seleccionar los 3 juegos principales
    top_3_games = top_games.head(3)

    # Crear el resultado en el formato deseado
    result = [{"Puesto {}: {}".format(i + 1, juego)} for i, juego in enumerate(top_3_games['item_name'])]

    return result


# Definir la ruta para la función UsersNotRecommend
@app.get("/users_not_recommend/")
def get_users_not_recommend(año: int = Query(..., description="Año para buscar los juegos menos recomendados")):
    result = UsersNotRecommend(año)
    return result

def UsersNotRecommend(año: int):
    # Obtener la ruta absoluta del archivo CSV en base al directorio actual del script
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Archivo2.csv'))
    # Cargar el archivo CSV utilizando la ruta absoluta
    df_RIG = pd.read_csv(file_path)
    
    # Filtrar el DataFrame por el año especificado y comentarios negativos
    filtered_df = df_RIG[(df_RIG['year_review'] == año) & (df_RIG['sentiment_analysis'] == 0)]

    # Verificar si hay datos disponibles
    if filtered_df.empty:
        return "No hay datos disponibles para ese año y comentarios negativos."

    # Agrupar las filas por el nombre del juego y contar las no recomendaciones
    game_not_recommendations = filtered_df.groupby('item_name')['sentiment_analysis'].count().reset_index()

    # Ordenar los juegos por el número de comentarios negativos en orden ascendente
    bottom_games = game_not_recommendations.sort_values(by='sentiment_analysis', ascending=True)

    # Seleccionar los 3 juegos principales (los menos recomendados)
    top_3_bottom_games = bottom_games.head(3)

    # Crear el resultado en el formato deseado
    result = [{"Puesto {}: {}".format(i + 1, juego)} for i, juego in enumerate(top_3_bottom_games['item_name'])]

    return result

@app.get("/sentiment_analysis/")
def get_sentiment_analysis(año: int = Query(..., description="Año para analizar el sentimiento de las reseñas")) -> Dict[str, int]:
    result = sentiment_analysis(año)
    return result

def sentiment_analysis(año: int) -> Dict[str, int]:  
    # Filtrar el DataFrame por el año especificado
    filtered_df = df_RIG[df_RIG['year_review'] == año]
    # Contar la cantidad de valores 0, 1 y 2 en la columna 'sentiment_analysis'
    negative_count = (filtered_df['sentiment_analysis'] == 0).sum()
    neutral_count = (filtered_df['sentiment_analysis'] == 1).sum()
    positive_count = (filtered_df['sentiment_analysis'] == 2).sum()
    # Crear el resultado en el formato deseado
    result = {"Negative": negative_count, "Neutral": neutral_count, "Positive": positive_count}
    return result

# Cargar el archivo CSV
# Obtener la ruta absoluta del archivo CSV en base al directorio actual del script
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Archivo_SCoseno.csv'))
# Cargar el archivo CSV utilizando la ruta absoluta
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
    juego_seleccionado = features[features['item_id'] == item_id]
    if juego_seleccionado.empty:
        raise HTTPException(status_code=404, detail="El item_id no se encuentra en los datos")
    cosine_sim = cosine_similarity(juego_seleccionado.iloc[:, :-2], features.iloc[:, :-2])
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_similar_games = sim_scores[1:(num_recomendaciones + 1)]
    recomendaciones = [features.iloc[i[0]]['item_name'] for i in top_similar_games]
    return recomendaciones