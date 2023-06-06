from Spotipy_func import user_vectors
from Mongo_pass import MONGO_STR
from pymongo import MongoClient
import pandas as pd


def connect_db(colec=None):
    """
    Función que establece conexión con la Base de Datos FestifyMe, y devuelve
    cursor de conexión a la colección (colec) especificada por el usuario
    """
    cursor = MongoClient(MONGO_STR)
    Festify = cursor.get_database('Festify')
    if colec is None:
        return Festify
    else:
        return Festify.get_collection(colec)


def insert_many(df, colec):
    """
    Función que inserta las filas de un DataFrame (df), en la colección colec
    de la Base de datos
    """
    colec.insert_many(df.to_dict(orient='records'))


def find_user(user):
    """
    Función que revisa si un usuario está cargado en la DB, si lo está devuelve
    el DataFrame con las playlist del usuario. Si no lo está devuelve un 
    DataFrame vacío
    """
    cursor = connect_db(colec='User_Features')
    query = cursor.find({'User_Id': user}, {'_id': 0})
    return pd.DataFrame(list(query))


def load_fest_feat():
    """Función que carga de la DB la tabla de los festivales 
    con sus features, y lo devuelve en DataFrame"""
    cursor = connect_db('Festival_Features')
    query = cursor.find({}, {'_id': 0})
    return pd.DataFrame(list(query))


def load_id_fest(id_fest):
    """
    Función que proporcionando un id de un Festival devuelve la información 
    del festval alojada en la tabla Festival
    """
    cursor = connect_db('Festival')
    query = cursor.find({'Id_Fest': id_fest}, {'_id': 0})
    return pd.DataFrame(list(query))


def load_band_feat(list_id_band):
    cursor = connect_db('Bands_Features')
    query = cursor.find({'Id_Band_Spotify': {"$in": list_id_band}}, {'_id': 0})
    return pd.DataFrame(list(query))


def check_rec(user):
    """
    Función que comprueba si existe el usuario en la colección Recomendations. 
    De ser así devuelve el DataFrame de recomendaciones, si no existe devuelve 
    DataFrame vacío
    """

    cursor = connect_db(colec='Recomendations')
    query = cursor.find({'User': user.lower()}, {'_id': 0})
    return pd.DataFrame(list(query))


def insert_rec(df):
    """
    Función que sube a la DB la tabla de recomendaciones (df) de un usuario
    """
    cursor = connect_db(colec='Recomendations')
    insert_many(df=df, colec=cursor)


def check_deploy(user):
    """
    Función que comprueba si existe el usuario en la colección Deploy.  
    Devuelve bool
    """

    cursor = connect_db(colec='Deploy')
    query = cursor.find({'User': user.lower()}, {'_id': 0})
    return pd.DataFrame(list(query))


def band_rec(df_rec):
    """
    Función que recibiendo una tabla de recomendaciones de un usuario, 
    devuelve un dataframe con la información de las bandas que aparecen en 
    dicha tabla
    """

    cursor = connect_db('Bands')
    query = cursor.find(
        {'Id_Spotify': {"$in": df_rec.Id_Band.unique().tolist()}}, {'_id': 0})
    band = pd.DataFrame(list(query))

    return band


def insert_deploy(df):
    """
    Función que sube a la DB la tabla deploy (df) de un usuario
    """
    cursor = connect_db(colec='Deploy')
    insert_many(df=df, colec=cursor)
