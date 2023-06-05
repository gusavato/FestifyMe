from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from sklearn.preprocessing import StandardScaler
from DB_func import *
from Spotify_id import *
import pandas as pd


def fest_similarity(user, top=10):
    """
    Función que recibiendo un usuario de Spotify, devuelve los 10 festivales 
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

    # Normalizamos
    simil_fest.loc[:] = StandardScaler().fit_transform(simil_fest[:])

    # Calculamos similitud aplicando cosenos
    distancias = squareform(pdist(simil_fest, 'cosine'))
    similitud = 1 / (1+distancias)
    df_similitud = pd.DataFrame(
        similitud, index=simil_fest.index, columns=simil_fest.index)

    playlist = vector.vector.Name_Playlist

    sim_json = []

    for p in playlist:
        dictio = dict(df_similitud.drop(
            columns=playlist).loc[p].sort_values(ascending=False)[0:5])
        sim_json.append({p: dictio})
