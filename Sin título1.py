# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:04:50 2024

@author: equipo
"""
import os as os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gp

#DATABASE

# Ruta del archivo subido
file_path = 'Downloads/TP FINAL PYTHON/Rosario F.xlsx'

excel_data = pd.ExcelFile(file_path)

# Obtener los nombres de las hojas
sheet_names = excel_data.sheet_names
sheet_names

# Leer los datos de la hoja "Hoja1"
df = excel_data.parse('Hoja1')

# Mostrar las primeras filas del DataFrame
df.head()

# Ver los valores únicos en la columna de intención de voto
unique_votes = df['INT DE VOTO X ESPACIO'].unique()
unique_votes

# Calcular las frecuencias de intención de voto
vote_counts = df['INT DE VOTO X ESPACIO'].value_counts()

# Mostrar las frecuencias
vote_counts

# Ver los valores únicos en la columna de edad
unique_ages = df['EDAD'].unique()
print=(unique_ages)

# Calcular las frecuencias de los rangos de edad
age_counts = df['EDAD'].value_counts()

# Crear un gráfico de columnas
plt.figure(figsize=(10, 6))
age_counts.plot(kind='bar', color= 'blue', edgecolor='grey')
plt.title('Distribución de Edades en la Muestra', fontsize=20)
plt.xlabel('Rango de Edad', fontsize=12)
plt.ylabel('Frecuencia', fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Mostrar el gráfico
plt.show()

import folium

# Crear un mapa centrado en las coordenadas promedio
mapa = folium.Map(
   location=[
            geo_data['Coord1__Latitude'].mean(), 
            geo_data['Coord1__Longitude'].mean() 
            ]
    zoom_start=12
)

# Añadir puntos al mapa
for _, row in geo_data.iterrows():
    folium.Marker(
        location=[row['Coord1__Latitude'], row['Coord1__Longitude']],
        popup=f"Edad: {row['EDAD']}, Género: {row['GENERO']}"
    ).add_to(mapa)

# Guardar el mapa interactivo en un archivo HTML
mapa.save('mapa_interactivo.html')