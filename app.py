import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from branca.colormap import linear

import streamlit as st

st.set_page_config(
    page_title="Evolución de tasas respuestas",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Decorador para cachear la carga y fusión de datos
@st.cache_data
def cargar_y_fusionar_datos(ruta_shp, ruta_csv):
    df = gpd.read_file(ruta_shp)
    tasasest = pd.read_csv(ruta_csv, index_col=0)
    df['CODCOMP_A'] = df['CODCOMP_A'].astype('Int64')
    tasasest = pd.merge(df, tasasest, left_on='CODCOMP_A', right_on='codcomp')
    tasasest['CODCOMP_A'] = tasasest['CODCOMP_A'].astype('string')
    tasasest['codcomp'] = tasasest['codcomp'].astype('string')
    tasasest = gpd.GeoDataFrame(tasasest)
    return tasasest

# Función para crear el mapa con folium
def crear_mapa(tasasest, tasasH, tasasMA, tasasR, location, zoom_start=20):
    m = folium.Map(location=location, zoom_start=15)
    colormap = linear.Reds_08.scale(0, 1)
    colormap.caption = "Tasa de Hechos"
    
    folium.GeoJson(
        tasasest,
        style_function=lambda feature: {
            "fillColor": colormap(feature['properties'][tasasH])
            if feature['properties'][tasasH] is not None
            else "transparent",
            "color": "black",
            "weight": 2,
            "dashArray": "5, 5",
            "fillOpacity": 0.5,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['codcomp', tasasH, tasasMA, tasasR],
            aliases=['Codcomp:', 'Tasa de Hechos:', 'Tasa de Morador Ausente:', 'Tasa de Rechazos:'],
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800,
        ),
    ).add_to(m)
    colormap.add_to(m)
    return m

# Carga y fusión de datos
ruta_shp = "./geodata/villadelcerro.shp"
tasasest1 = cargar_y_fusionar_datos(ruta_shp, './tasas_data/tasasest1.csv')
tasasest2 = cargar_y_fusionar_datos(ruta_shp, './tasas_data/tasasest2.csv')
tasasest3 = cargar_y_fusionar_datos(ruta_shp, './tasas_data/tasasest3.csv')

location = [-34.8840204, -56.2506134]

# Creación de mapas
m1 = crear_mapa(tasasest1, 'tasaH1', 'tasaMA1', 'tasaR1', location)
m2 = crear_mapa(tasasest2, 'tasaH2', 'tasaMA2', 'tasaR2', location)
m3 = crear_mapa(tasasest3, 'tasaH3', 'tasaMA3', 'tasaR3', location)

# Opciones para visualizar el mapa en Streamlit
# Continuación de tu código...

# Opciones para visualizar el mapa en Streamlit, basado en la selección del usuario

# Define las columnas para el layout
left_column, right_column = st.columns([3, 1])  # Ajusta las proporciones según necesites

# Usar la columna izquierda para el selectbox y el mapa
with left_column:
    etapa_seleccionada = st.selectbox(
        "Selecciona la etapa que deseas visualizar:",
        ('Etapa 1', 'Etapa 2', 'Etapa 3')
    )

    # Decide qué mapa mostrar basado en la selección de la etapa
    if etapa_seleccionada == 'Etapa 1':
        mapa_seleccionado = m1
    elif etapa_seleccionada == 'Etapa 2':
        mapa_seleccionado = m2
    else:
        mapa_seleccionado = m3
    
    # Mostrar el mapa
    return_on_hover = True  # Asumiendo que siempre quieres esta funcionalidad activada
    output = st_folium(mapa_seleccionado, width=1000, height=500, return_on_hover=return_on_hover)

# Usar la columna derecha para mostrar la información del tooltip
with right_column:
    st.write("## Información de la manzana:")
    # Muestra la información del último tooltip interactuado
    if "last_object_clicked_tooltip" in output:
        st.write(output["last_object_clicked_tooltip"])
    else:
        st.write("Pasa el mouse sobre el mapa para ver los tooltips.")
