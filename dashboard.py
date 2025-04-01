import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from io import StringIO
import plotly.express as px
import plotly.graph_objects as go
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

archivo_csv_vi = "/workspaces/Prueba/EDIT_S_VI_2016_2017.csv"
archivo_csv_vii = "/workspaces/Prueba/EDITS_VII_2018_2019.csv"
archivo_csv_viii = "/workspaces/Prueba/Estructura_EDITS_VIII_2020_2021.csv"
df_2016 = pd.read_csv("/workspaces/Prueba/EDIT_S_VI_2016_2017.csv", sep=';')
df_2018 = pd.read_csv("/workspaces/Prueba/EDITS_VII_2018_2019.csv" , sep=';')
df_2020 = pd.read_csv("/workspaces/Prueba/Estructura_EDITS_VIII_2020_2021.csv", sep=';')
df_vi = pd.read_csv(archivo_csv_vi, sep=";")
df_vii = pd.read_csv(archivo_csv_vii, sep=";")
df_viii = pd.read_csv(archivo_csv_viii, sep=";")
df_vi['Periodo'] = '2016-2017'
df_vii['Periodo'] = '2018-2019'
df_viii['Periodo'] = '2020-2021'
# Unir los dos datasets
df = pd.concat([df_vi, df_vii, df_viii], ignore_index=True)
# Mostrar contenido según la selección
# st.write(f"### {selected}") 

def estadisticos(columna):
  # Asegurar que los datos sean numéricos
  df[columna] = pd.to_numeric(df[columna], errors='coerce')

  # Filtrar datos por período
  s2016 = df[df['Periodo'] == "2016-2017"][columna]
  s2018 = df[df['Periodo'] == "2018-2019"][columna]
  s2020 = df[df['Periodo'] == "2020-2021"][columna]

  # Definir función para calcular estadísticas
  def calcular_estadisticas(data):
      return pd.Series({
          "Cantidad": data.count(),
          "Media": data.mean(),
          "Mediana": data.median(),
          "Moda": data.mode().iloc[0] if not data.mode().empty else np.nan,
          "Varianza": data.var(),
          "Desviación Estándar": data.std(),
          "Asimetría (Cola)": data.skew(),
          "Curtosis": data.kurt(),
          "Mínimo": data.min(),
          "Máximo": data.max(),
          "Percentil 10": data.quantile(0.10),
          "Percentil 90": data.quantile(0.90)
      }).round(2)

  # Calcular estadísticas por período
  stats_2016 = calcular_estadisticas(s2016)
  stats_2018 = calcular_estadisticas(s2018)
  stats_2020 = calcular_estadisticas(s2020)

  # Combinar estadísticas en un solo DataFrame
  final_stats = pd.DataFrame({
      "2016-2017": stats_2016,
      "2018-2019": stats_2018,
      "2020-2021": stats_2020
  })

  # Mostrar la tabla final
  return final_stats

if selected =="EDITS 2016-2017/2018-2019/2020-2021":
    st.write("# EDITS 2016-2017")
    st.write("Exploración de DataFrame")
    st.dataframe(df_2016.head(10))
    buffer = StringIO()
    df_2016.info(buf=buffer)
    info= buffer.getvalue()
    st.code(info, language='text')
    st.write("# EDITS 2018-2019")
    st.write("Exploración de DataFrame")
    st.dataframe(df_2018.head(10))
    buffer = StringIO()
    df_2018.info(buf=buffer)
    info= buffer.getvalue()
    st.code(info, language='text')
    st.write("# EDITS 2020-2021")
    st.write("Exploración de DataFrame")
    st.dataframe(df_2020.head(10))
    buffer = StringIO()
    df_2020.info(buf=buffer)
    info= buffer.getvalue()
    st.code(info, language='text')

elif selected == "1. Empresas que introdujeron bienes o servicios nuevos.":
    st.title("# I1R1C1N:Servicios o bienes nuevos únicamente para su empresa. Si=1, No=2")
    df_grouped = df.groupby('Periodo')['I1R1C1N'].value_counts(normalize=True).unstack() * 100
    df_grouped = df_grouped.rename(columns={1: 'Sí', 2: 'No'})

    # Resetear el índice para que 'Periodo' sea una columna regular
    df_grouped.reset_index(inplace=True)

    # Crear el gráfico de barras apiladas con Plotly
    fig = px.bar(df_grouped, x='Periodo', y=['Sí', 'No'], 
                title='Porcentaje de empresas con bienes o servicios nuevos por año',
                labels={'Periodo': 'Año', 'value': 'Porcentaje', 'variable': 'Introdujo Innovación'},
                color='variable', 
                color_discrete_sequence=["#a50026", "#3b4cc0"],
                text_auto=True)

    # Agregar etiquetas de porcentaje a las barras
    fig.update_traces(texttemplate='%{value:.1f}%', textposition='inside', hoverinfo='text')

    # Mostrar el gráfico interactivo en Streamlit
    st.plotly_chart(fig)

        # Crear DataFrame de innovación similar al original
    df_innovacion = pd.DataFrame({
        '2016-2017': df_2016['I1R1C1N'].value_counts(),
        '2018-2019': df_2018['I1R1C1N'].value_counts(),
        '2020-2021': df_2020['I1R1C1N'].value_counts()
    }).rename(index={2: 'No', 1: 'Sí'})

    # Preparar los datos para el gráfico
    df_innovacion = df_innovacion.T  # Transponemos para que los periodos sean columnas

    # Crear el gráfico apilado con Plotly
    fig = go.Figure()

    # Agregar las barras para cada periodo
    fig.add_trace(go.Bar(
        x=df_innovacion.index,
        y=df_innovacion['Sí'],
        name='Sí',
        marker_color="#a50026",  # Color personalizado (puedes cambiarlo)
        text=df_innovacion['Sí'],  # Etiquetas de los valores
        textposition='inside',  # Las etiquetas estarán dentro de las barras
    ))

    fig.add_trace(go.Bar(
        x=df_innovacion.index,
        y=df_innovacion['No'],
        name='No',
        marker_color='#3b4cc0',  # Color personalizado (puedes cambiarlo)
        text=df_innovacion['No'],  # Etiquetas de los valores
        textposition='inside',  # Las etiquetas estarán dentro de las barras
    ))

    # Personalizar la disposición del gráfico
    fig.update_layout(
        title='Comparación de Innovación por Año',
        xaxis_title='Periodo',
        yaxis_title='Cantidad de Empresas',
        barmode='stack',  # Apilamos las barras
        xaxis={'tickmode': 'array', 'tickvals': df_innovacion.index, 'ticktext': df_innovacion.index},  # Aseguramos que las etiquetas en el eje x sean correctas
        legend_title='¿Innovación en el Mercado?',
        template='plotly_dark'  # Opcional: Puedes cambiar el tema de colores
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    st.write("Estadísticos:")
    est=estadisticos('I1R1C1N')
    st.dataframe(est)


elif selected == "2. N° promedio de bienes/servicios nuevos por periodo.":
    st.title("# I1R1C2N:Número total de innovaciones en servicios o bienes nuevos únicamente para su empresa 2018-2019")
    df['I1R1C2N'] = pd.to_numeric(df['I1R1C2N'], errors='coerce')
    df = df.dropna(subset=['I1R1C2N'])

    # Calcular los promedios por periodo
    promedios_nuevos = df.groupby('Periodo')['I1R1C2N'].mean().round()

    # Crear la figura
    fig = go.Figure()

    # Agregar las barras para cada periodo
    fig.add_trace(go.Bar(
        x=promedios_nuevos.index,
        y=promedios_nuevos.values,
        marker_color=["#a50026", "#3b4cc0", "#d73027"],  # Colores personalizados
        text=promedios_nuevos.values,  # Etiquetas de los valores
        textposition='outside',  # Las etiquetas estarán fuera de las barras
    ))

    # Personalización del gráfico
    fig.update_layout(
        title='Promedio de bienes/servicios nuevos por empresa',
        xaxis_title='Periodo',
        yaxis_title='Promedio',
        showlegend=False,  # No mostrar la leyenda ya que solo hay una serie
        font=dict(size=17),
    )

    # Mostrar el gráfico
    st.plotly_chart(fig)
    st.write("Estadísticos:")
    est=estadisticos('I1R1C2N')
    st.dataframe(est)


elif selected == "3. Número total de innovaciones por periodo.":
    st.title("# I1R4C2N:Número total de innovaciones de servicios o bienes nuevos 2018-2019")
    # Asegúrate de que df ya está filtrado
    df['I1R4C2N'] = pd.to_numeric(df['I1R4C2N'], errors='coerce')

    # Calcular el total de innovaciones por periodo
    total_innovaciones = df.groupby('Periodo')['I1R4C2N'].sum()

    # Crear la figura
    fig = go.Figure()

    # Agregar las barras para cada periodo
    fig.add_trace(go.Bar(
        x=total_innovaciones.index,
        y=total_innovaciones.values,
        marker_color=["#a50026", "#3b4cc0", "#d73027"],  # Colores personalizados
        text=total_innovaciones.values,  # Etiquetas de los valores
        textposition='outside',  # Las etiquetas estarán fuera de las barras
    ))

    # Personalización del gráfico
    fig.update_layout(
        title='Total de innovaciones de bienes/servicios nuevos',
        xaxis_title='Periodo',
        yaxis_title='Cantidad total de innovaciones',
        showlegend=False,  # No mostrar la leyenda ya que solo hay una serie
        font=dict(size=12),
    )

    # Mostrar el gráfico
    st.plotly_chart(fig)

    st.write("Estadísticos:")
    est=estadisticos('I1R4C2N')
    st.dataframe(est)
 
elif selected == "4.Innovación por actividad económica.":
    # Código o acción para "4.Innovación por actividad económica."
    pass
elif selected == "5.Empresas por tipología y periodo.":
    # Código o acción para "5.Empresas por tipología y periodo."
    pass
elif selected == "6.Empresas con bienes mejorados.":
    # Código o acción para "6.Empresas con bienes mejorados."
    pass
elif selected == "7.Impacto en la innovación.":
    # Código o acción para "7.Impacto en la innovación."
    pass