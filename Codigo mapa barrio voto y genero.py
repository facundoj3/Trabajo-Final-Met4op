# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 20:29:58 2024

@author: usuariopc
"""

import pandas as pd
import folium
import json

# Rutas de los archivos
datos_path = r"C:/Users/usuariopc/Downloads/TP FINAL PYTHON/rosario.xlsx"
barrios_csv_path = r"C:/Users/usuariopc/Downloads/TP FINAL PYTHON/barrios_rosario.csv"

# Cargar datos
df_votos = pd.read_excel(datos_path)
df_barrios = pd.read_csv(barrios_csv_path)

# Verificar las columnas disponibles
print("Columnas del archivo Excel:")
print(df_votos.columns)
print("\nColumnas del archivo CSV:")
print(df_barrios.columns)

# Ajustar la columna para la unión
# Cambiar 'RADIO' a la columna correcta (ejemplo: 'BARRIO' o similar)
clave_union = 'BARRIO'  # Cambiar a la columna correcta si no es RADIO

# Revisar si la columna existe en ambos archivos
if clave_union not in df_votos.columns or clave_union not in df_barrios.columns:
    raise ValueError(f"La columna '{clave_union}' no está presente en ambos archivos.")

# Continuar con el procesamiento solo si existe una columna en común
frecuencias_voto = (
    df_votos.groupby([clave_union, "INT DE VOTO X ESPACIO"])["GENERO"]
    .count()
    .reset_index()
    .rename(columns={"GENERO": "FRECUENCIA"})
)

espacios_por_barrio = (
    frecuencias_voto.groupby(clave_union)
    .apply(lambda x: x.loc[x["FRECUENCIA"].idxmax()])
    .reset_index(drop=True)
)

porcentajes_voto = (
    frecuencias_voto.groupby(clave_union)
    .apply(lambda x: x.assign(PORCENTAJE=(x["FRECUENCIA"] / x["FRECUENCIA"].sum()) * 100))
    .reset_index(drop=True)
)

porcentajes_genero = (
    df_votos.groupby([clave_union, "GENERO"])["GENERO"]
    .count()
    .unstack(fill_value=0)
    .reset_index()
)

porcentajes_genero["TOTAL"] = porcentajes_genero["Femenino"] + porcentajes_genero["Masculino"]
porcentajes_genero["Femenino (%)"] = (porcentajes_genero["Femenino"] / porcentajes_genero["TOTAL"]) * 100
porcentajes_genero["Masculino (%)"] = (porcentajes_genero["Masculino"] / porcentajes_genero["TOTAL"]) * 100

# Fusionar datos para usarlos en el mapa
barrios_data = df_barrios.merge(
    espacios_por_barrio, left_on=clave_union, right_on=clave_union, how="left"
).merge(
    porcentajes_genero, left_on=clave_union, right_on=clave_union, how="left"
)

# Crear el mapa base
mapa = folium.Map(location=[-32.94682, -60.63932], zoom_start=12)

# Agregar barrios al mapa
for _, row in barrios_data.iterrows():
    geojson_data = json.loads(row["GEOJSON"])
    
    popup_text = f"""
    <b>{row['BARRIO']}</b><br>
    Espacio con mayor intención de voto: {row['INT DE VOTO X ESPACIO']}<br>
    Frecuencia: {row['FRECUENCIA']} ({row['PORCENTAJE']:.2f}%)<br>
    Masculino: {row['Masculino (%)']:.2f}%<br>
    Femenino: {row['Femenino (%)']:.2f}%<br>
    """
    
    folium.GeoJson(
        geojson_data,
        name=row["BARRIO"],
        style_function=lambda x: {
            "color": "black",
            "weight": 1,
            "fillColor": "none",
            "fillOpacity": 0.5,
        },
        popup=folium.Popup(popup_text, max_width=300),
    ).add_to(mapa)

# Guardar el mapa
mapa.save("mapa_intencion_voto_por_barrio.html")
