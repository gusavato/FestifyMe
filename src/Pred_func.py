from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from sklearn.preprocessing import StandardScaler
from DB_func import *
from Spotify_id import *
from Spotipy_func import *
import pandas as pd
import numpy as np


def get_simil(df):
    """
    Función que recibe un dataframe, en el que cada registro es un vector.
    Devuelve matriz de similitud
    """
    # Normalizamos
    df.loc[:] = StandardScaler().fit_transform(df[:])

    # Creamos matriz de similitud
    distancias = squareform(pdist(df, 'cosine'))
    similitud = 1 / (1+distancias)
    df_similitud = pd.DataFrame(
        similitud, index=df.index, columns=df.index)

    return df_similitud


def fest_similarity(user, top=8):
    """
    Función que recibiendo un usuario de Spotify, devuelve los 15 festivales 
    más similares por cada playlist del usuario
    """

    # Comprobamos si tenemos registro del usuario en la DB
    vector = find_user(user.lower())

    # Generamos vector de usauario y lo cargamos en caso de no tener
    # registro

    if vector.shape[0] == 0:
        vector = user_vectors(user)
        insert_many(vector, connect_db(colec='User_Features'))

    # Cargamos tabla Festival_Features

    fest_feat = load_fest_feat()

    # Construimos matriz de similitud
    vector_compare = vector.drop(
        columns=['User_Id', 'Id_Playlist']).set_index('Name_Playlist')

    fest_compare = fest_feat.drop(
        columns=['Explicit', 'Artist_Popularity']).set_index('Id_Fest')

    simil_fest = pd.concat([vector_compare, fest_compare], axis=0)

    # Obtenemos matriz de similitud
    df_similitud = get_simil(simil_fest)

    playlist = vector.Name_Playlist

    recomendation = []

    # Asociamos recomendación a festival
    for p in playlist:
        dictio = dict(df_similitud.drop(
            columns=playlist).loc[p].sort_values(ascending=False)[0:top])
        recomendation.append({p: dictio})

    df_rec = pd.DataFrame([(k, k1, v1) for d in recomendation for k, v in d.items() for k1, v1 in v.items()],
                          columns=['Playlist', 'ID_Fest', 'Similarity'])

    return df_rec


def artist_similarity(user):
    """
    Función que al introducir un usuario de Spotify devuelve un datafrane con 
    las afinidades por festival y lista
    """

    # Obtenemos los festivales recomendados para el usuario
    df_sim = fest_similarity(user)

    # Obtenemos todas las canciones de las playlist del usuario
    playlist_user = get_full_tracks(user)

    # Obtenemos vector del usuario de la base de datos
    vector = find_user(user)

    # Inicializamos un DataFrame vacio
    df_artist_rec = pd.DataFrame(columns=['Playlist',
                                          'Fest_Id',
                                          'Band',
                                          'Affinity'])

    # Recorremos todas las playlist del usuario
    for plist in vector.Name_Playlist:

        # Por cada Playlist vemos los festivales recomendados
        for fest_id in df_sim[df_sim.Playlist == plist]['ID_Fest']:

            # Obtenemos las bandas del festival que no están en las playlist
            fest = load_id_fest(fest_id)
            fest = fest[~fest.Id_Spotify.isin(playlist_user.Id_Band_Spotify)]

            # Obtenemos las features de las bandas
            bands = load_band_feat(fest.Id_Spotify.tolist())
            bands = pd.merge(left=fest,
                             left_on='Id_Spotify',
                             right=bands,
                             right_on='Id_Band_Spotify')

            # Creamos Dataframe para obtener similitud
            bands_comp = bands.drop(columns=['Lat',
                                             'Long',
                                             'Explicit',
                                             'Artist_Popularity',
                                             'Id_Fest']).set_index('Bands')._get_numeric_data()

            vector_comp = vector.drop(columns=['User_Id',
                                               'Id_Playlist']).set_index('Name_Playlist').loc[plist]

            vector_comp = pd.DataFrame(np.reshape(vector_comp, [1, -1]),
                                       columns=bands_comp.columns,
                                       index=[plist])

            simil = pd.concat([vector_comp, bands_comp])

            simil = get_simil(simil)

            # Obtenemos recomendaciones
            rec = dict(simil.iloc[0, 1:].sort_values(
                ascending=False)[:5])

            df = pd.DataFrame([(plist, fest_id, k, v) for k, v in rec.items()],
                              columns=['Playlist',
                                       'Fest_Id',
                                       'Band',
                                       'Affinity'])

            df_artist_rec = pd.concat(
                [df_artist_rec, df]).reset_index(drop=True)

    return df_artist_rec
