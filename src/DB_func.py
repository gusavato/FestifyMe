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
