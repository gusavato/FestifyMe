import streamlit as st
import pandas as pd
from Pred_func import *
import folium
from streamlit_folium import st_folium
from streamlit_folium import folium_static

fest_click = None
st.set_page_config(layout="wide")

# Barra lateral
st.sidebar.markdown(
    """
    <h2 style='font-size: 40px; color: #8EF984;'>FestifyMe</h2>
    """,
    unsafe_allow_html=True
)

user = st.sidebar.text_input('Usuario')
if user is '':
    user = 'gus_57'

# Obtenemos dataframe usuario

df = build_deploy(user)

if df is None:
    df = build_deploy('gus_57')
    st.sidebar.markdown("""
    <h2 style='font-size: 24px; color: red;'>Usuario no encontrado</h2>
    """,
                        unsafe_allow_html=True)
    user = 'gus_57'


# Ponemos título a la página

st.markdown(
    f"""
    <h1 style='font-size: 48px; color: #8EF984;'>FestifyMe for {user}</h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h5 style='font-size: 24px; color: #8EF984;'>Casi 100 festivales, más de 1500 grupos. 
    FestifyMe soluciona el dilema de cada verano- A qué festival ir y qué conciertos ver.
    </h5>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='font-size: 20px; color: #8EF984;'>
    Disfruta de la recomendación de festivales y grupos nuevos según las 
    canciones de tus playlist de Spotify.</br> 
    </div>
    """,
    unsafe_allow_html=True)

st.markdown('***')

# Creamos columnas mapa Festival

col_map, col_fest = st.columns([45, 55], gap='large')

with col_map:
    playlist = st.selectbox('Filtrar por Playlist', df.Playlist.unique())

    # Creamos mapa
    mapa = folium.Map(location=[40.0167278, -1.7033387],
                      zoom_start=5, tiles='CartoDB dark_matter')

    # Dataframe de la playlist seleccionada
    df_playlist = df[df.Playlist == playlist]

    # Añadimos marcadores al mapa
    for i in df_playlist.Id_Fest.unique():

        fest = df_playlist[df_playlist.Id_Fest == i]
        folium.Marker(location=fest[['Lat', 'Long']].mean(),
                      tooltip=f'<div style="font-size: 15px; color:#007013;"><strong>{fest.Festival.iloc[0]}</strong></div>',
                      icon=folium.Icon(color='green', icon="fa-brands fa-spotify", prefix='fa')).add_to(mapa)

    # Mostramos mapa y creamos variable ret para controlar los clicks
    ret = st_folium(mapa, height=500, width=800)


# Variable que nos devuelve el último festival clickado
fest_click = ret['last_object_clicked_tooltip']

# Establecemos valor por defecto para fest_click. Para que tenga
# valor al inicio del programa
if fest_click is None:
    fest_click = df.Festival.unique()[0]

# Creamos df con la información de la playlist y del festival clickado
df_click = df[(df.Playlist == playlist) & (df.Festival == fest_click)]

# Añadimos festivales recomendados al sidebar
f_rec = df[['Playlist', 'Festival', 'Similarity']].drop_duplicates()
f_rec = f_rec[f_rec.Playlist == playlist]
zip_f_rec = list(zip(f_rec.Festival, f_rec.Similarity))

st.sidebar.markdown(
    """
            <h4 style='font-size: 25px;color:#5787DE'>Festivales Recomendados</h4>
            """,
    unsafe_allow_html=True
)

st.sidebar.subheader(zip_f_rec[0][0])
st.sidebar.write(f'{round(zip_f_rec[0][1]*100,2)} %')
st.sidebar.subheader(zip_f_rec[1][0])
st.sidebar.write(f'{round(zip_f_rec[1][1]*100,2)} %')
st.sidebar.subheader(zip_f_rec[2][0])
st.sidebar.write(f'{round(zip_f_rec[2][1]*100,2)} %')
st.sidebar.subheader(zip_f_rec[3][0])
st.sidebar.write(f'{round(zip_f_rec[3][1]*100,2)} %')
st.sidebar.subheader(zip_f_rec[4][0])
st.sidebar.write(f'{round(zip_f_rec[4][1]*100,2)} %')
st.sidebar.subheader(zip_f_rec[5][0])
st.sidebar.write(f'{round(zip_f_rec[5][1]*100,2)} %')
st.sidebar.subheader(zip_f_rec[6][0])
st.sidebar.write(f'{round(zip_f_rec[6][1]*100,2)} %')
st.sidebar.subheader(zip_f_rec[7][0])
st.sidebar.write(f'{round(zip_f_rec[7][1]*100,2)} %')


with col_fest:

    # Cremaos columnas para el nombre del festival selccionado y
    # para su afinidad
    col_name_fest, col_similarity = st.columns([775, 225], gap='large')

    with col_name_fest:
        try:
            festival_name = df_click.Festival.unique()[0]
        except:
            festival_name = zip_f_rec[0][0]
        st.markdown(
            f"""
            <h1 style='font-size: 42px;'>{festival_name}</h1>
            """,
            unsafe_allow_html=True
        )

    with col_similarity:
        try:
            sim = round(df_click.Similarity.unique()[0]*100, 1)
        except:
            df_click = df[(df.Playlist == playlist) &
                          (df.Festival == festival_name)]
            sim = round(df_click.Similarity.unique()[0]*100, 1)

        st.metric(label="**Afinidad**", value=f'{sim}%')

    st.markdown("""
                <h3 style='font-size: 32px;'>Bandas recomendadas por descubrir</h3>
                """,
                unsafe_allow_html=True)
    st.markdown('***')

    col_im_band_rec, col_band_rec, col_affin = st.columns(
        [1, 3, 1], gap='small')

    band_rec = list(
        zip(df_click['Image'], df_click['Bands'], df_click['Affinity'], df_click['Url']))

    with col_im_band_rec:
        image_width = 60
        st.image(band_rec[0][0], width=image_width)
        st.image(band_rec[1][0], width=image_width)
        st.image(band_rec[2][0], width=image_width)
        st.image(band_rec[3][0], width=image_width)
        st.image(band_rec[4][0], width=image_width)

    with col_band_rec:
        band_name = band_rec[0][1]
        band_website = band_rec[0][3]
        st.markdown(f"## [{band_name}]({band_website})")
        band_name = band_rec[1][1]
        band_website = band_rec[1][3]
        st.markdown(f"## [{band_name}]({band_website})")
        band_name = band_rec[2][1]
        band_website = band_rec[2][3]
        st.markdown(f"## [{band_name}]({band_website})")
        band_name = band_rec[3][1]
        band_website = band_rec[3][3]
        st.markdown(f"## [{band_name}]({band_website})")
        band_name = band_rec[4][1]
        band_website = band_rec[4][3]
        st.markdown(f"## [{band_name}]({band_website})")

    with col_affin:
        st.header(f'{round(band_rec[0][2]*100,1)} %')
        st.header(f'{round(band_rec[1][2]*100,1)} %')
        st.header(f'{round(band_rec[2][2]*100,1)} %')
        st.header(f'{round(band_rec[3][2]*100,1)} %')
        st.header(f'{round(band_rec[4][2]*100,1)} %')

# Cargamos la tabla con el cartel del festival seleccionado
id_fest = int(df_click.Id_Fest.unique()[0])
df_fest = load_id_fest(id_fest)

# OBtenemos las bandas del festival
list_id_band = df_fest.Id_Spotify.unique().tolist()
df_bands = pd.read_parquet('../data/bands.parquet')
df_bands = df_bands[df_bands.Id_Spotify.isin(list_id_band)]

# Ordenamos por popularidad
df_bands = df_bands.sort_values('Popularity', ascending=False)

band_fest = list(
    zip(df_bands['Image'], df_bands['Bands'], df_bands['Popularity'], df_bands['Url']))


# Cartel del festival


st.markdown("""
            <h3 style='font-size: 32px;'>Cabezas de Cartel</h3>
            """,
            unsafe_allow_html=True)
st.markdown('***')


col_im_band, col_band, col_pop = st.columns(
    [1, 3, 2], gap='small')

with col_im_band:
    image_width = 60
    st.image(band_fest[0][0], width=image_width)
    st.image(band_fest[1][0], width=image_width)
    st.image(band_fest[2][0], width=image_width)
    st.image(band_fest[3][0], width=image_width)
    st.image(band_fest[4][0], width=image_width)

with col_band:
    band_n = band_fest[0][1]
    band_w = band_fest[0][3]
    st.markdown(f"## [{band_n}]({band_w})")
    band_n = band_fest[1][1]
    band_w = band_fest[1][3]
    st.markdown(f"## [{band_n}]({band_w})")
    band_n = band_fest[2][1]
    band_w = band_fest[2][3]
    st.markdown(f"## [{band_n}]({band_w})")
    band_n = band_fest[3][1]
    band_w = band_fest[3][3]
    st.markdown(f"## [{band_n}]({band_w})")
    band_n = band_fest[4][1]
    band_w = band_fest[4][3]
    st.markdown(f"## [{band_n}]({band_w})")

with col_pop:
    st.header(band_fest[0][2])
    st.header(band_fest[1][2])
    st.header(band_fest[2][2])
    st.header(band_fest[3][2])
    st.header(band_fest[4][2])
