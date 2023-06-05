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
            dictio['Id'] = item['id']
            dictio['Name'] = item['name']
            dictio['Playlist_Url'] = item['external_urls']['spotify']
            dictio['API_href'] = item['href']

            lst.append(dictio)

        # Comprobamos que el usuario no tenga más de 50 listas
        if response['next']:
            patron = r"offset=(\d+)"
            offset = int(re.findall(
                patron, response['next'].split('?')[-1])[0])
            response = sp.user_playlists(user, offset=offset)
        else:
            are_next = False

    if len(lst) != 1:
        df = pd.DataFrame(lst)
    else:
        df = pd.DataFrame(lst, index=[0])

    return df


def get_playlist_tracks(id_):
    """
    Función que recibiendo un id de una playllist, devuelve un dataframe 
    con las features de cada canción 
    """
    sp = get_connection()
    try:
        tracks = sp.playlist_tracks(id_)
    except:
        return None

    lst = []
    are_next = True
    while are_next:
        for track in tracks['items']:
            try:
                dictio = dict()
                dictio['Track'] = track['track']['name']
                dictio['Id_Track'] = track['track']['id']
                dictio['Bands'] = track['track']['artists'][0]['name']
                dictio['Id_Band_Spotify'] = track['track']['artists'][0]['id']
                dictio['Track_Popularity'] = track['track']['popularity']

                lst.append(dictio)
            except:
                pass

        if tracks['next']:
            patron = r"offset=(\d+)"
            offset = int(re.findall(
                patron, tracks['next'].split('?')[-1])[0])
            tracks = sp.playlist_tracks(id_, offset=offset)
        else:
            are_next = False

    if len(lst) != 1:
        df = pd.DataFrame(lst)
    else:
        df = pd.DataFrame(lst, index=[0])

    return df


def get_full_tracks(user):
    """
    Función que dándole un usuario de Spotify, devuleve un ud DataFrame con
    todas las canciones de sus playlist
    """

    df_playlist = get_user_playlists(user)

    if df_playlist is None:
        return None

    df_tracks = pd.DataFrame(columns=['User', 'User_Id', 'Name_Playlist',
                                      'Id_Playlist', 'Track', 'Id_Track',
                                      'Bands', 'Id_Band_Spotify',
                                      'Track_Popularity'])

    for row in df_playlist.itertuples():
        df = get_playlist_tracks(row.Id)
        df[['User', 'User_Id', 'Name_Playlist', 'Id_Playlist']] = [
            row.User, row.User_Id, row.Name, row.Id]
        df = df[['User', 'User_Id', 'Name_Playlist', 'Id_Playlist', 'Track',
                 'Id_Track', 'Bands', 'Id_Band_Spotify', 'Track_Popularity']]
        df_tracks = pd.concat([df_tracks, df], axis=0).reset_index(drop=True)

    return df_tracks


def get_audio_features(list_tracks):
    """
    Función que devuelve las audio_features de un lista de canciones
    """

    sp = get_connection()

    # La API de Spotify sólo permite consulvestorstas de 100 canciones max por
    # consulta
    lst = []
    for n in range(len(list_tracks)//100 + 1):
        lst.append(sp.audio_features(list_tracks[n*100:(n+1)*100]))

    # Convertimos el array a 1D
    features = []
    for l in lst:
        for track in l:
            features.append(track)

    df_features = pd.DataFrame(features)

    return df_features


def user_vectors(user):
    """
    Función que devuelve el vector con los parámetros del usuario en función 
    de las features de las canciones de sus playlist públicas
    """

    df_tracks = get_full_tracks(user)

    if df_tracks is None:
        return None

    # Obtenemos un dataframe con todas las canciones de todas las playlist
    unique_tracks = df_tracks.Id_Track.unique()

    df_features = get_audio_features(unique_tracks)

    df_features = pd.merge(left=df_tracks, left_on='Id_Track',
                           right=df_features, right_on='id', how='left')

    # Creamos df con los vectores
    vectors = pd.concat([df_features[['Id_Playlist', 'Track_Popularity']],
                         df_features._get_numeric_data(
    )], axis=1).groupby('Id_Playlist', as_index=False).mean()

    # Añadimos Id de usuario
    vectors.insert(loc=0, column='User_Id',
                   value=df_features['User_Id'].unique()[0])

    # Añadimos fila con el vector de todas las listas

    vectors.loc[vectors.shape[0]] = vectors.loc[0]
    vectors.loc[vectors.shape[0]-1, 'Id_Playlist'] = 'All'
    vectors.loc[vectors.shape[0]-1,
                'danceability':] = vectors._get_numeric_data().mean()

    vectors.columns = [x.title() for x in vectors.columns]

    return vectors
