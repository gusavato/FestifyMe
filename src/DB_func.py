from Spotipy_func import user_vectors
from Mongo_pass import MONGO_STR
from pymongo import MongoClient


def connect_db():
    """
    Función que establece conexión con la Base de Datos FestifyMe
    """
    cursor = MongoClient(MONGO_STR)
    Festify = cursor.get_database('Festify')
    return Festify


def insert_many(df, colec):
    """
    Función que inserta las filas de un DataFrame (df), en la colección colec
    de la Base de datos
    """
    colec.insert_many(df.to_dict(orient='records'))
