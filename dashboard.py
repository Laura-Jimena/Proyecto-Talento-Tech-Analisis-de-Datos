import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import nbformat
from nbconvert import PythonExporter


# Cargar el notebook
with open("/Co_proyecto_copia1.ipynb", "r", encoding="utf-8") as f:
    notebook = nbformat.read(f, as_version=4)
# Convertir el notebook a código Python
exporter = PythonExporter()
script, _ = exporter.from_notebook_node(notebook)
# Ejecutar el código del notebook en este script
exec(script)
# Ahora puedes acceder a los DataFrames del notebook directamente
# print(df.head())  # Asumiendo que df está definido en el notebook

# Configurar la barra lateral con estilos oscuros
with st.sidebar:
    selected = option_menu(
        menu_title=None,  # Sin título
        options=["EDITS 2016-2017/2018-2019/2020-2021","1. Empresas que introdujeron bienes o servicios nuevos.", "2. N° promedio de bienes/servicios nuevos por periodo.", "3.Número total de innovaciones por periodo", 
                 "4.Innovación por actividad económica.", "5.Empresas por tipología y periodo.","6.Empresas con bienes mejorados.","7.Impacto en la innvación."],
        icons=["bi-calendar","bi-lightbulb", "bi-award", "bi-globe", "bi-file-earmark-bar-graph", "bi-briefcase","bi-journal-check","bi-graph-up"],  # Iconos de Bootstrap
        menu_icon="cast",  # Icono de la barra de menú
        default_index=0,  # Selección predeterminada
        styles={
            "container": {"padding": "5px", "background-color": "#212529"},  # Fondo oscuro
            "icon": {"color": "white", "font-size": "20px"},  # Estilo de iconos
            "nav-link": {"font-size": "16px", "color": "white", "text-align": "left"},
            "nav-link-selected": {"background-color": "#6c757d","font-weight": "normal"},  # Color al seleccionar
        }
    )

# Mostrar contenido según la selección
st.write(f"### {selected}") 

if selected =="EDITS 2016-2017/2018-2019/2020-2021":
    data = {
        'Periodo': ['2020', '2020', '2021', '2021', '2022', '2022'],
        'I1R1C1N': [1, 2, 1, 2, 1, 2],
        'Cantidad': [50, 50, 60, 40, 70, 30]
    }
    df = pd.DataFrame(data)
    df_grouped = df.groupby('Periodo')['I1R1C1N'].value_counts(normalize=True).unstack() * 100
    df_grouped = df_grouped.rename(columns={1: 'Sí', 2: 'No'})

    # Mostrar DataFrame en Streamlit
    st.dataframe(df_grouped)

    # Graficar
    fig, ax = plt.subplots(figsize=(8, 6))
    df_grouped.plot(kind='bar', stacked=True, colormap='coolwarm', ax=ax)

    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', label_type='center', fontsize=10, color='white')

    plt.title('Porcentaje de empresas con bienes o servicios nuevos por año')
    plt.xlabel('Periodo')
    plt.ylabel('Porcentaje')
    plt.legend(title="Introdujo Innovación")

    # Mostrar gráfico
    st.pyplot(fig)

elif selected == "1. Empresas que introdujeron bienes o servicios nuevos.":
    st.write("Graf 1")
elif selected == "2. N° promedio de bienes/servicios nuevos por periodo.":
    # Aquí agregas otro gráfico específico para esta opción
    st.write("Aquí va la gráfica del N° promedio de bienes o servicios nuevos por periodo.")

elif selected == "3. Número total de innovaciones por periodo":
    # Agrega otro gráfico para esta sección
    st.write("Aquí va la gráfica del número total de innovaciones por periodo.")

 # Muestra la opción seleccionada
# data = {
#     'Periodo': ['2020', '2020', '2021', '2021', '2022', '2022'],
#     'I1R1C1N': [1, 2, 1, 2, 1, 2],
#     'Cantidad': [50, 50, 60, 40, 70, 30]
# }
# df = pd.DataFrame(data)


# df_grouped = df.groupby('Periodo')['I1R1C1N'].value_counts(normalize=True).unstack() * 100
# df_grouped = df_grouped.rename(columns={1: 'Sí', 2: 'No'})
# st.dataframe(df_grouped)

# # Graficar en Streamlit
# fig, ax = plt.subplots(figsize=(8, 6))
# df_grouped.plot(kind='bar', stacked=True, colormap='coolwarm', ax=ax)

# for container in ax.containers:
#     ax.bar_label(container, fmt='%.1f%%', label_type='center', fontsize=10, color='white')

# plt.title('Porcentaje de empresas con bienes o servicios nuevos por año')
# plt.xlabel('Periodo')
# plt.ylabel('Porcentaje')
# plt.legend(title="Introdujo Innovación")

# # Mostrar en Streamlit
# st.pyplot(fig)