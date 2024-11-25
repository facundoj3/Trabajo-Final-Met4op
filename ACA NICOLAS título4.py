# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 20:14:41 2024

@author: usuariopc
"""

import pandas as pd
import folium
import json

# Ruta de los archivos
datos_path = r"C:/Users/usuariopc/Downloads/TP FINAL PYTHON/rosario.xlsx"
barrios_csv_path = r"C:/Users/usuariopc/Downloads/TP FINAL PYTHON/barrios_rosario.csv"

# Cargar datos principales
df = pd.read_excel(datos_path)

# Crear mapa base centrado en Rosario
center_lat = df['Coord1__Latitude'].mean()
center_lon = df['Coord1__Longitude'].mean()
mapa_combinado = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Colores para género
colores_genero = {
    "Masculino": "blue",
    "Femenino": "deeppink",
    None: "gray"
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

# Agregar los cuadrados con información de intención de voto y género
for _, row in df.iterrows():
    lat = row['Coord1__Latitude']
    lon = row['Coord1__Longitude']
    genero = row['GENERO']
    voto = row['INT DE VOTO X ESPACIO']

    # Crear un cuadrado que combina los colores de género e intención de voto
    square = [
        [lat + 0.0021, lon - 0.0021],
        [lat + 0.0021, lon + 0.0021],
        [lat - 0.0021, lon + 0.0021],
        [lat - 0.0021, lon - 0.0021]
    ]

    folium.Polygon(
        locations=square,
        color=colores_genero.get(genero, "gray"),  # Color del borde según género
        fill=True,
        fill_color=colores_voto.get(voto, "gray"),  # Color de relleno según intención de voto
        fill_opacity=0.7,
        popup=folium.Popup(f"Edad: {row['EDAD']}<br>Género: {genero}", max_width=200)
    ).add_to(mapa_combinado)

# Cargar datos de barrios
df_barrios = pd.read_csv(barrios_csv_path)

# Agregar límites de barrios al mapa
for _, row in df_barrios.iterrows():
    geojson_data = json.loads(row['GEOJSON'])  # Convertir GeoJSON de texto a objeto JSON

    folium.GeoJson(
        geojson_data,
        name=row['BARRIO'],
        style_function=lambda x: {
            'color': 'black',
            'weight': 1,
            'fillColor': 'none',  # Sin relleno para no ocultar los datos de intención de voto y género
            'fillOpacity': 0.5
        },
        popup=folium.Popup(f"Barrio: {row['BARRIO']}", max_width=300)
    ).add_to(mapa_combinado)

# Guardar el mapa combinado
mapa_combinado.save("mapa_combinado_con_voto_genero_barrios.html")
