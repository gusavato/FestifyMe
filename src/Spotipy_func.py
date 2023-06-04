import pandas as pd
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from Spotify_id import *


def get_connection():
    """
    Función que establece conexión con la API de Spotify.
    Devuelve objeto spotipy.Spotify() que permite realzar 
    las consultas con la API
    """
    global Client_ID, Client_secret
    auth_manager = SpotifyClientCredentials(
        client_id=Client_ID, client_secret=Client_secret)

    sp = spotipy.Spotify(auth_manager=auth_manager)

    return sp


def get_user(user):
    """
    Función que devuelve la información de un usuario de Spotify.
    Recibe nombre de usuario y devueleve diccionario con:
    Display_name en Spotify
    Id de Spotify
    Url de pagina en spotify
    """

    sp = get_connection()
    try:
        response = sp.user(user)
    except:
        return None

    return {'Display_name': response['display_name'],
            'Id': response['id'],
            'Url': response['external_urls']['spotify']
            }


def get_user_playlists(user):
    """
    Función que recibiendo un usuario de Spotify, devuelve información 
    de las playlists públicas del usuario
    """
    # Establecemos conexión
    sp = get_connection()
    try:
        response = sp.user_playlists(user)
    except:
        return None

    if not response['items']:
        return None

    # Obtenemos información del usuario

    user_dict = get_user(user)

    # Obtenemos información de las playlists
    lst = []
    are_next = True
    while are_next:
        for item in response['items']:
            dictio = dict()
            dictio['User'] = user_dict['Display_name']
            dictio['User_Id'] = user_dict['Id']
            dictio['User_Url'] = user_dict['Url']
            dictio['Name'] = item['name']
            dictio['Playlist_Url'] = item['external_urls']['spotify']
            dictio['API_href'] = item['href']
            dictio['Id'] = item['id']

            lst.append(dictio)

        # Comprobamos que el usuario no tenga más de 50 listas
        if response['next']:
            patron = r"offset=(\d+)"
            offset = int(re.findall(
                patron, response['next'].split('?')[-1])[0])
            response = sp.user_playlists(user, offset=offset)
        else:
            are_next = False

    if lst != 1:
        df = pd.DataFrame(lst)
    else:
        df = pd.DataFrame(lst, index=[0])

    return df
