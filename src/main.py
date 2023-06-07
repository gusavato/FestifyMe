import streamlit as st
import pandas as pd
from Pred_func import *
import folium
from streamlit_folium import st_folium
from streamlit_folium import folium_static

st.set_page_config(layout="wide")

st.sidebar.title('Festify')
user = st.sidebar.text_input('user')
if user is '':
    user = 'gus_57'

df = build_deploy(user)


st.title('Festify')


col_map, col_fest = st.columns([45, 55], gap='large')

with col_map:
    playlist = st.selectbox('Filtrar Playlist', df.Playlist.unique())

    mapa = folium.Map(location=[40.0167278, -1.7033387],
                      zoom_start=5, tiles='CartoDB dark_matter')

    df_playlist = df[df.Playlist == playlist]

    for i in df_playlist.Id_Fest.unique():

        # popup_content = f'''
        # <div style="font-size: 16px; color: #007013;">
        #     <strong>{fest.Similarity.iloc[0]*100}%</strong><br>
        #     <strong>Bands:</strong> {fest.Bands.iloc[0]}<br>
        #     <strong>Affinity:</strong> {fest.Affinity.iloc[0]}
        # </div>
        # '''

        fest = df_playlist[df_playlist.Id_Fest == i]
        folium.Marker(location=fest[['Lat', 'Long']].mean(),
                      popup=folium.Popup(fest.Bands.iloc[0], max_width=400),
                      tooltip=f'<div style="font-size: 15px; color:#007013;"><strong>{fest.Festival.iloc[0]}</strong></div>',
                      icon=folium.Icon(color='green', icon="fa-brands fa-spotify", prefix='fa')).add_to(mapa)

    ret = st_folium(mapa, height=450, width=800)


fest_click = ret['last_object_clicked_tooltip']

if fest_click is None:
    fest_click = df.Festival.unique()[0]

df_click = df[(df.Playlist == playlist) & (df.Festival == fest_click)]
f_rec = df[['Playlist', 'Festival', 'Similarity']].drop_duplicates()
f_rec = f_rec[f_rec.Playlist == playlist]
zip_f_rec = list(zip(f_rec.Festival, f_rec.Similarity))

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
    col_name_fest, col_similarity = st.columns([775, 225], gap='large')

    with col_name_fest:
        st.title(df_click.Festival.unique()[0], anchor='right')

    with col_similarity:
        sim = round(df_click.Similarity.unique()[0]*100, 1)
        st.metric(label="**Afinidad**", value=f'{sim}%')

    col_im_band_rec, col_band_rec, col_affin = st.columns(
        [1, 3, 1], gap='small')

    band_rec = list(
        zip(df_click['Image'], df_click['Bands'], df_click['Affinity']))

    with col_im_band_rec:
        image_width = 60
        st.image(band_rec[0][0], width=image_width)
        st.image(band_rec[1][0], width=image_width)
        st.image(band_rec[2][0], width=image_width)
        st.image(band_rec[3][0], width=image_width)
        st.image(band_rec[4][0], width=image_width)

    with col_band_rec:
        st.header(band_rec[0][1])
        st.header(band_rec[1][1])
        st.header(band_rec[2][1])
        st.header(band_rec[3][1])
        st.header(band_rec[4][1])

    with col_affin:
        st.header(f'{round(band_rec[0][2]*100,1)} %')
        st.header(f'{round(band_rec[1][2]*100,1)} %')
        st.header(f'{round(band_rec[2][2]*100,1)} %')
        st.header(f'{round(band_rec[3][2]*100,1)} %')
        st.header(f'{round(band_rec[4][2]*100,1)} %')

id_fest = int(df_click.Id_Fest.unique()[0])
df_fest = load_id_fest(id_fest)

list_id_band = df_fest.Id_Spotify.unique().tolist()
cursor = connect_db('Bands')
query = cursor.find({'Id_Spotify': {"$in": list_id_band}}, {
                    '_id': 0, 'API_href': 0, 'API_Uri': 0})
df_bands = pd.DataFrame(list(query))
df_bands = df_bands.sort_values('Popularity', ascending=False)


band_fest = list(
    zip(df_bands['Image'], df_bands['Bands'], df_bands['Popularity']))


col_im_band, col_band, col_pop = st.columns(
    [1, 3, 1], gap='small')

with col_im_band:
    image_width = 60
    st.image(band_fest[0][0], width=image_width)
    st.image(band_fest[1][0], width=image_width)
    st.image(band_fest[2][0], width=image_width)
    st.image(band_fest[3][0], width=image_width)
    st.image(band_fest[4][0], width=image_width)

with col_band:
    st.header(band_fest[0][1])
    st.header(band_fest[1][1])
    st.header(band_fest[2][1])
    st.header(band_fest[3][1])
    st.header(band_fest[4][1])

with col_pop:
    st.header(band_fest[0][2])
    st.header(band_fest[1][2])
    st.header(band_fest[2][2])
    st.header(band_fest[3][2])
    st.header(band_fest[4][2])
