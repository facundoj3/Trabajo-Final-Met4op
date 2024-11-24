# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 19:47:00 2024

@author: usuariopc
"""

import pandas as pd
import folium

# Ruta del archivo
file_path = r"C:/Users/usuariopc/Downloads/TP FINAL PYTHON/rosario.xlsx"

# Cargar el archivo Excel
df = pd.read_excel(file_path)

# Inspeccionar las primeras filas para asegurarnos de que las columnas son correctas
print(df.head())

# Crear un mapa base centrado en una ubicación inicial (ajustar según los datos)
center_lat = df['Coord1__Longitude'].mean()
center_lon = df['Coord1__Longitude'].mean()
mapa_genero = folium.Map(location=[center_lat, center_lon], zoom_start=12)


# Mapa 1: Dispersión por "GENERO"
for _, row in df.iterrows():
    if row['GENERO'] == 'Masculino':
        color = 'blue'
    elif row['GENERO'] == 'Femenino':
        color = 'pink'
    else:
        color = 'gray'
    folium.CircleMarker(
        location=[row['Coord1__Latitude'], row['Coord1__Longitude']],
        radius=5,
        color=color,
        fill=True,
        fill_opacity=0.7,
    ).add_to(mapa_genero)

# Crear el popup con información
    popup_info = f"Edad: {row['EDAD']}<br>Género: {row['GENERO']}"
    
    folium.CircleMarker(
        location=[row['Coord1__Latitude'], row['Coord1__Longitude']],
        radius=5,
        color=color,
        fill=True,
        fill_opacity=0.7,
        popup=folium.Popup(popup_info, max_width=300)
        ).add_to(mapa_genero)
# Guardar el mapa interactivo
mapa_genero.save("mapa_genero2.html")
# Crear un mapa base para INT DE VOTO X ESPACIO
mapa_voto = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Definir colores para cada categoría
colores_voto = {
    "LIBERTARIOS": "purple",
    "JxC": "yellow",
    "FdT": "lightblue",
    "FIT": "red",
    "PNK": "blue",
    "OTROS": "gray",
    "NOSABE/NOCONTESTA": "white"
}

# Mapa 2: Dispersión por "INT DE VOTO X ESPACIO"
for _, row in df.iterrows():
    color = colores_voto.get(row['INT DE VOTO X ESPACIO'], 'gray')  # Valor por defecto gris
    folium.CircleMarker(
        location=[row['Coord1__Latitude'], row['Coord1__Longitude']],
        radius=5,
        color=color,
        fill=True,
        fill_opacity=0.7,
    ).add_to(mapa_voto)
#POPUP
    popup_info = f"Edad: {row['EDAD']}<br>Género: {row['GENERO']}"
    
    folium.CircleMarker(
        location=[row['Coord1__Latitude'], row['Coord1__Longitude']],
        radius=5,
        color=color,
        fill=True,
        fill_opacity=0.7,
        popup=folium.Popup(popup_info, max_width=300)
    ).add_to(mapa_voto)
# Guardar el mapa interactivo
mapa_voto.save("mapa_voto22.html")

df = pd.read_excel(file_path)

# Crear un mapa base centrado en una ubicación inicial
center_lat = df['Coord1__Latitude'].mean()
center_lon = df['Coord1__Longitude'].mean()
mapa_combinado = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Colores para los géneros
colores_genero = {
    "Masculino": "blue",
    "Femenino": "pink",
    None: "gray",  # Para datos faltantes
}

# Colores para intención de voto
colores_voto = {
    "LIBERTARIOS": "purple",
    "JxC": "yellow",
    "FdT": "lightblue",
    "FIT": "red",
    "PNK": "blue",
    "OTROS": "gray",
    "NOSABE/NOCONTESTA": "white"
}

for _, row in df.iterrows():
    # Obtener colores
    color_genero = colores_genero.get(row['GENERO'], 'gray')
    color_voto = colores_voto.get(row['INT DE VOTO X ESPACIO'], 'gray')
    
    # Crear el popup con información
    popup_info = f"Edad: {row['EDAD']}<br>Género: {row['GENERO']}<br>Intención de voto: {row['INT DE VOTO X ESPACIO']}"
    
    # Coordenadas para el cuadrado
    lat, lon = row['Coord1__Latitude'], row['Coord1__Longitude']
    square = [
        [lat + 0.0020, lon - 0.0020],  # Esquina superior izquierda
        [lat + 0.0020, lon + 0.0020],  # Esquina superior derecha
        [lat - 0.0020, lon + 0.0020],  # Esquina inferior derecha
        [lat - 0.0020, lon - 0.0020],  # Esquina inferior izquierda
    ]
    
    # Dibujar el cuadrado en el mapa
    folium.Polygon(
        locations=square,
        color=color_genero,  # Borde según el género
        fill=True,
        fill_color=color_voto,  # Relleno según intención de voto
        fill_opacity=0.7,
        popup=folium.Popup(popup_info, max_width=300)
    ).add_to(mapa_combinado)

# Guardar el mapa interactivo
mapa_combinado.save("mapa_combinado.html")

import json

# Cargar datos del mapa principal
mapa_combinado = folium.Map(location=[-32.94682, -60.63932], zoom_start=12)  # Ejemplo: Rosario, ajusta según tus datos

# Cargar datos de barrios
barrios_csv_path = r"C:/Users/usuariopc/Downloads/TP FINAL PYTHON/barrios_rosario.csv"
df_barrios = pd.read_csv(barrios_csv_path)

# Agregar barrios al mapa
for _, row in df_barrios.iterrows():
    # Convertir el GeoJSON de texto a objeto JSON
    geojson_data = json.loads(row['GEOJSON'])  # Asegúrate de que la columna sea válida

    # Agregar el polígono del barrio al mapa
    folium.GeoJson(
        geojson_data,
        name=row['BARRIO'],
        style_function=lambda x: {
            'color': 'black',
            'weight': 1,
            'fillColor': 'none',  # Sin relleno
            'fillOpacity': 0.5
        },
        popup=folium.Popup(f"Barrio: {row['BARRIO']}", max_width=300)
    ).add_to(mapa_combinado)

# Guardar el mapa con los barrios
mapa_combinado.save("mapa_combinado_con_barrios.html")