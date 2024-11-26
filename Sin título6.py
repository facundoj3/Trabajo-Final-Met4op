import pandas as pd
from shapely.geometry import shape
from geopy.distance import geodesic
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Cargar datos
votos_df = pd.read_excel('C:/Users/usuariopc/Downloads/TP FINAL PYTHON/rosario.xlsx')
parques_df = pd.read_csv('C:/Users/usuariopc/Downloads/TP FINAL PYTHON/espacios_verdes_parques_json.csv')

# Convertir columna GEOJSON a geometrías válidas
parques_df['geometry'] = parques_df['GEOJSON'].apply(eval).apply(shape)

# Obtener centroides de los parques
parques_df['centroid'] = parques_df['geometry'].apply(lambda geom: (geom.centroid.y, geom.centroid.x))
parques_coords = parques_df['centroid'].tolist()

# Calcular distancia mínima a parques para cada votante
def min_distance_to_parks(voter_coord, parks_coords):
    return min(geodesic(voter_coord, park_coord).kilometers for park_coord in parks_coords)

votos_df['distance_to_park'] = votos_df.apply(
    lambda row: min_distance_to_parks((row['Coord1__Latitude'], row['Coord1__Longitude']), parques_coords), axis=1
)

# Determinar cercanía (menos de 0.5 km)
threshold_distance = 0.5
votos_df['near_park'] = votos_df['distance_to_park'] < threshold_distance

# Crear tabla de contingencia
votos_df['is_libertario'] = votos_df['INT DE VOTO X ESPACIO'] == 'LIBERTARIOS'
contingency_table = pd.crosstab(votos_df['near_park'], votos_df['is_libertario'])

# Realizar prueba chi-cuadrado
chi2, p, dof, expected = chi2_contingency(contingency_table)

# Calcular proporciones
proportion_near = contingency_table.loc[True, True] / contingency_table.loc[True].sum() * 100
proportion_far = contingency_table.loc[False, True] / contingency_table.loc[False].sum() * 100

print("Resultados:")
print(f"Chi-cuadrado: {chi2:.2f}, p-valor: {p:.4f}")
print(f"Proporción de votos 'LIBERTARIOS' cerca de parques: {proportion_near:.2f}%")
print(f"Proporción de votos 'LIBERTARIOS' lejos de parques: {proportion_far:.2f}%")

# Visualización
labels = ['Cerca de parque', 'Lejos de parque']
values = [proportion_near, proportion_far]

plt.bar(labels, values, color=['green', 'gray'])
plt.title("Proporción de votos 'LIBERTARIOS' por cercanía a parques")
plt.ylabel('Porcentaje (%)')
plt.show()
