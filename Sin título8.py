# Paquetes
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# Diccionario de categorías de colores (puedes ajustar colores específicos para género y edad si lo deseas)
categorias_genero = {
    'Masculino': 'skyblue',
    'Femenino': 'pink',
    'Otros': 'gray'
}

categorias_edad = {
    '16 a 25': 'aliceblue',
    '26 a 35': 'skyblue',
    '36 a 45': 'royalblue',
    '46 a 55': 'slateblue',
    '56 y mas': 'indigo'
}

# Cargar datos
data = pd.read_excel('C:/Users/usuariopc/Downloads/TP FINAL PYTHON/rosario.xlsx')
data.columns = [col.lower() for col in data.columns]

# Gráfico de torta para composición de género
def grafico_composicion_genero(data):
    genero_data = data['genero'].value_counts()
    colors = [categorias_genero.get(cat, 'gray') for cat in genero_data.index]
    genero_data.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=colors, figsize=(6, 6))
    plt.title("Composición de Género")
    plt.ylabel('')  # Para ocultar la etiqueta del eje Y
    plt.show()

# Gráfico de torta para composición de edad
def grafico_composicion_edad(data):
    edad_data = data['edad'].value_counts()
    colors = [categorias_edad.get(cat, 'gray') for cat in edad_data.index]
    edad_data.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=colors, figsize=(6, 6))
    plt.title("Composición de Edad")
    plt.ylabel('')  # Para ocultar la etiqueta del eje Y
    plt.show()


# Gráfico de barras para composición de edad
def grafico_composicion_edad(data):
    edad_data = data['edad'].value_counts()
    colors = [categorias_edad.get(cat, 'gray') for cat in edad_data.index]
    edad_data.plot(kind='bar', figsize=(6, 6))
    plt.title("Composición de Edad")
    plt.ylabel('')  # Para ocultar la etiqueta del eje Y
    plt.show()
    
# Llamar a las funciones para graficar
grafico_composicion_genero(data)
grafico_composicion_edad(data)