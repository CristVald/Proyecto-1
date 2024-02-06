# Importaciones
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import functions_api as fa
from fastapi import HTTPException

import importlib
importlib.reload(fa)

# Se instancia la aplicación
app = FastAPI()

# Funciones
@app.get(path = '/developer',
          description = """ <font color="blue">
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el nombre del desarrollador en el box abajo.<br>
                        3. Scrollear a "Resposes" para ver la cantidad de items y porcentaje de contenido Free por año de ese desarrollador.
                        </font>
                        """,
         tags=["Consultas Generales"])
def developer(desarrollador: str = Query(..., 
                            description="Desarrollador del videojuego", 
                            example='Valve')):
    return fa.developer(desarrollador)


@app.get(path = '/userdata',
          description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el user_id en el box abajo.<br>
                        3. Scrollear a "Resposes" para ver la cantidad de dinero gastado por el usuario, el porcentaje de recomendación que realiza el usuario y cantidad de items que tiene el mismo.
                        </font>
                        """,
         tags=["Consultas Generales"])
def userdata(user_id: str = Query(..., 
                                description="Identificador único del usuario", 
                                example="EchoXSilence")):
        
    return fa.userdata(user_id)
    
    
@app.get(path = '/userforgenre',
          description = """ <font color="blue">
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el género en el box abajo.<br>
                        3. Scrollear a "Resposes" para ver Top 5 de usuarios con más horas de juego en el género dado, con su URL y user_id.
                        </font>
                        """,
         tags=["Consultas Generales"])
def userforgenre(genero: str = Query(..., 
                            description="Género del videojuego", 
                            example='Simulation')):
    return fa.userforgenre(genero)


@app.get(path = '/best_developer_year',
          description = """ <font color="blue">
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el género en el box abajo.<br>
                        3. Scrollear a "Resposes" para ver el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado.
                        </font>
                        """,
         tags=["Consultas Generales"])
def best_developer_year(anio: int = Query(..., 
                            description="Mejores 3 desarrolladores del año", 
                            example= 2012)):
    return fa.best_developer_year(anio)



@app.get(path = '/developer_reviews_analysis',
          description = """ <font color="blue">
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el género en el box abajo.<br>
                        3. Scrollear a "Resposes" para ver un diccionario con el nombre del desarrollador como llave y la cantidad de opiniones positivas o negativas.
                        </font>
                        """,
         tags=["Consultas Generales"])
def developer_reviews_analysis(desarrolladora: str = Query(..., 
                            description="Cantidad de opiniones positivas o negativas", 
                            example= "Smartly Dressed Games")):
    return fa.developer_reviews_analysis(desarrolladora)

