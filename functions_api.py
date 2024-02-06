## FUNCIONES A UTILIZAR EN app.py

# Importaciones
import pandas as pd
import numpy as np
import operator
from fastapi import HTTPException

# Datos a usar

df_user_reviews = pd.read_parquet("df_user_reviews.parquet")
df_user_data = pd.read_parquet("df_user_data.parquet")
df_user_for_genre = pd.read_parquet("df_userforgenre.parquet")
df_item_developer_year = pd.read_parquet("df_item_developer_year.parquet")
df_best_developer = pd.read_parquet("df_best_developer.parquet")
df_pivot_norm = pd.read_parquet("df_pivot_norm.parquet")
df_item_sim = pd.read_parquet("df_item_sim.parquet")
df_user_sim = pd.read_parquet("df_user_sim.parquet")


      
def developer(desarrollador: str):
    '''
    Esta función devuelve información sobre una empresa desarrolladora de videojuegos.
         
    Args:
        desarrollador (str): Nombre del desarrollador de videojuegos.
    
    Returns:
        dict: Un diccionario que contiene información sobre la empresa desarrolladora.
            - 'cantidad_por_año' (dict): Cantidad de items desarrollados por año.
            - 'porcentaje_gratis_por_año' (dict): Porcentaje de contenido gratuito por año según la empresa desarrolladora.
    '''
    try:
        # Filtramos el dataframe por desarrollador de interés
        data_filtrada = df_item_developer_year[df_item_developer_year["developer"] == desarrollador]

        # La cantidad de items por año
        cantidad_por_año = data_filtrada.groupby("release_year")["item_id"].count()

        # La cantidad de elementos gratis por año
        cantidad_gratis_por_año = data_filtrada[data_filtrada["price"] == 0.0].groupby("release_year")["item_id"].count()

        # El porcentaje de elementos gratis por año
        porcentaje_gratis_por_año = (cantidad_gratis_por_año / cantidad_por_año * 100).fillna(0).astype(int)

        result_dict = {
            "cantidad_por_año": cantidad_por_año.to_dict(),
            "porcentaje_gratis_por_año": porcentaje_gratis_por_año.to_dict()
        }

        return result_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")



def userdata(user_id:str):
    '''
    Esta función devuelve información sobre un usuario según su 'user_id'.
         
    Args:
        user_id (str): Identificador único del usuario.
    
    Returns:
        dict: Un diccionario que contiene información sobre el usuario.
            - 'cantidad_dinero' (int): Cantidad de dinero gastado por el usuario.
            - 'porcentaje_recomendacion' (float): Porcentaje de recomendaciones realizadas por el usuario.
            - 'total_items' (int): Cantidad de items que tiene el usuario.
    '''
    

    try:
        # Filtramos por el usuario de interés
        user = df_user_reviews[df_user_reviews["user_id"] == user_id]

        # Verificamos si se encontraron datos para el usuario
        if user.empty:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # La cantidad de dinero gastado para el usuario de interés
        cantidad = int(df_user_data[df_user_data["user_id"]== user_id]["price"].iloc[0].item())

        # Buscamos el count_item para el usuario de interés    
        conteo_items = int(df_user_data[df_user_data["user_id"]== user_id]["items_count"].iloc[0].item())

        # Total de recomendaciones realizadas por el usuario de interés
        total_recomendaciones = user["reviews_recommend"].sum()

        # Total de reviews realizada por todos los usuarios
        total_reviews = len(df_user_reviews["user_id"].unique())

        # Porcentaje de recomendaciones realizadas por el usuario de interés
        porcentaje_recomendaciones = (total_recomendaciones / total_reviews) * 100

        return {
            "cantidad_dinero": cantidad,
            "porcentaje_recomendacion": round(porcentaje_recomendaciones, 2),
            "total_items": conteo_items
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

def userforgenre(genero):
    '''
    Esta función devuelve el top 5 de usuarios con más horas de juego en un género específico, junto con su URL de perfil y ID de usuario.
         
    Args:
        genero (str): Género del videojuego.
    
    Returns:
        dict: Un diccionario que contiene el top 5 de usuarios con más horas de juego en el género dado, junto con su URL de perfil y ID de usuario.
            - 'user_id' (str): ID del usuario.
            - 'user_url' (str): URL del perfil del usuario.
    '''
    
    try:
        # Filtramos el DataFrame por el género dado
        genre_data = df_user_for_genre[df_user_for_genre["genres"] == genero]

        # Verificamos si hay datos para el género
        if genre_data.empty:
            return f"No hay datos para el género {genero}."

        # Usuario con más horas jugadas para ese género
        top_user = genre_data.loc[genre_data["played_hours"].idxmax()]["user_id"]

        # Lista de acumulación de horas jugadas por año
        hours_by_year = genre_data.groupby("release_year")["played_hours"].sum().reset_index()

        hours_by_year = hours_by_year.rename(columns={"release_year": "Año", "played_hours": "Horas"})

        hours_list = hours_by_year.to_dict(orient="records")

        # Diccionario de retorno
        result = {
            "Usuario con más horas jugadas para Género {}".format(genero): top_user,
            "Horas jugadas": hours_list
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


def best_developer_year(anio):
    
    try:
        # Filtramos por el año dado y solo con comentarios recomendados y positivos
        df_filtrado = df_best_developer[(df_best_developer["year"] == anio) & (df_best_developer["reviews_recommend"] == True) & (df_best_developer["sentiment_analysis"] == 2)]

        # Verificamos si hay datos para el año
        if df_filtrado.empty:
            return f"No hay datos para el año {anio}."

        # Agrupamos por desarrollador y contamos la cantidad de juegos recomendados
        desarrolladores_top = df_filtrado.groupby("developer")["item_id"].count().reset_index()

        # Verificamos si hay desarrolladores encontrados
        if desarrolladores_top.empty:
            return f"No hay desarrolladores encontrados para el año {anio}."

        # Ordenamos en orden descendente y seleccionar los tres primeros
        desarrolladores_top = desarrolladores_top.sort_values(by="item_id", ascending=False).head(3)

        # Creamos el resultado en el formato deseado
        resultado = [{"Puesto " + str(i+1): desarrollador} for i, desarrollador in enumerate(desarrolladores_top['developer'])]

        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

def developer_reviews_analysis(desarrolladora):
    
    try:
        # Filtrar por desarrolladora
        df_filtrado = df_best_developer[df_best_developer["developer"] == desarrolladora]

        if df_filtrado.empty:
            return f"No hay datos para la desarrolladora {desarrolladora}."

        # Contar la cantidad de registros con análisis de sentimiento 0, 1 y 2
        conteo_sentimientos = df_filtrado["sentiment_analysis"].value_counts()

        # Convertir los valores de conteo_sentimientos a tipos nativos de Python
        resultado = {
            desarrolladora: {
                "Negative": int(conteo_sentimientos.get(0, 0)),
                "Positive": int(conteo_sentimientos.get(2, 0))
            }
        }

        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
