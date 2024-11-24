# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 14:35:01 2024

@author: equipo
"""

import pandas as pd

# Cargar el archivo Excel
file_path = "C:/Users/equipo/Downloads/TP FINAL PYTHON/Rosario F.xlsx"  # Cambia por la ruta de tu archivo
databaserosario = pd.read_excel(file_path)

# Listar los nombres de las columnas
print(databaserosario.columns)

import folium

# Cargar los datos del archivo Excel
file_path = "C:/Users/equipo/Downloads/TP FINAL PYTHON/Rosario F.xlsx"  # Cambia esta ruta por la ubicación del archivo
databaserosario = pd.read_excel(file_path)

# Filtrar datos con coordenadas válidas (ajusta los nombres de las columnas si es necesario)
geo_data = databaserosario.dropna(subset=['Coord1__Latitude','Coord1__Longitude'])

# Crear un mapa centrado en las coordenadas promedio
mapa = folium.Map(
    location=[geo_data['Coord1__Latitude'].mean(), geo_data['Coord1__Longitude'].mean()],
    zoom_start=12
)

# Añadir puntos al mapa
for _, row in geo_data.iterrows():
    folium.Marker(
        location=[row['Coord1__Latitude'], row['Coord1__Longitude']],
        popup=f"Información: {row.to_dict()}"  # Puedes personalizar el contenido
    ).add_to(mapa)

# Guardar el mapa en un archivo HTML
mapa.save("mapa_interactivo.html")


print("Mapa creado y guardado como mapa_interactivo.html")
mapa.save("mapa_interactivo.html")
print("Mapa guardado exitosamente.")
