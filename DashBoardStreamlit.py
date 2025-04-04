import streamlit as st
from streamlit_option_menu import option_menu
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from io import StringIO
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide")
st.sidebar.title("Impacto de la innovación en procesos organizacionales y participación de mercado en Colombia.")
with st.sidebar:
    selected = option_menu(
        menu_title=None,  # Sin título
        options=["1. Empresas que introdujeron bienes o servicios nuevos.", "2. N° promedio de bienes/servicios nuevos por periodo.", "3.Número total de innovaciones por periodo.", 
                 "4.Innovación por actividad económica por periodo.", "5.Empresas que innovan por tipología y periodo.","6.Empresas con bienes mejorados.","7.Impacto en la innvación.","8.Empresas que introdujeron un bien o servicio unicamente en el mercado internacional.","9.Impacto en la innovación de las empresas de servicios."],
        icons=["bi-lightbulb", "bi-award", "bi-calendar-range", "bi-file-earmark-bar-graph", "bi-briefcase","bi-journal-check","bi-graph-up","bi-globe","bi-briefcase"],  # Iconos de Bootstrap
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
df_2016 = pd.read_csv("/workspaces/Prueba/EDIT_S_VI_2016_2017.csv", sep=';',low_memory=False)
df_2018 = pd.read_csv("/workspaces/Prueba/EDITS_VII_2018_2019.csv" , sep=';',low_memory=False)
df_2020 = pd.read_csv("/workspaces/Prueba/Estructura_EDITS_VIII_2020_2021.csv", sep=';',low_memory=False)
df_vi = pd.read_csv(archivo_csv_vi, sep=";",low_memory=False)
df_vii = pd.read_csv(archivo_csv_vii, sep=";",low_memory=False)
df_viii = pd.read_csv(archivo_csv_viii, sep=";",low_memory=False)
df_vi['Periodo'] = '2016-2017'
df_vii['Periodo'] = '2018-2019'
df_viii['Periodo'] = '2020-2021'
# Unir los dos datasets
df = pd.concat([df_vi, df_vii, df_viii], ignore_index=True)
# Mostrar contenido según la selección
# st.write(f"### {selected}") 
emp=pd.read_excel("/workspaces/Prueba/ciiu_actividad_economica.xlsx")
df_emp=pd.merge(df,emp, left_on='CIIU4', right_on='Indice',how="inner")
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

# if selected =="EDITS 2016-2017/2018-2019/2020-2021":
#     st.write("# IMPACTO DE LA INNOVACIÓN EN PROCESOS ORGANIZACIONALES Y PARTICIPACIÓN DE MERCADO EN COLOMBIA.")
#     st.write("## EDITS 2016-2017")
#     st.write("### Exploración del DataFrame:")
#     st.dataframe(df_2016.head(10))
#     buffer = StringIO()
#     df_2016.info(buf=buffer)
#     info= buffer.getvalue()
#     st.code(info, language='text')
#     st.write("## EDITS 2018-2019")
#     st.write("### Exploración del DataFrame:")
#     st.dataframe(df_2018.head(10))
#     buffer = StringIO()
#     df_2018.info(buf=buffer)
#     info= buffer.getvalue()
#     st.code(info, language='text')
#     st.write("## EDITS 2020-2021")
#     st.write("### Exploración del DataFrame:")
#     st.dataframe(df_2020.head(10))
#     buffer = StringIO()
#     df_2020.info(buf=buffer)
#     info= buffer.getvalue()
#     st.code(info, language='text')

if selected == "1. Empresas que introdujeron bienes o servicios nuevos.":
    st.title("I1R1C1N:Servicios o bienes nuevos.(Mercado Nacional y/o Internacional.) Si=1, No=2")
    
    # Agrupar datos y calcular porcentajes
    df_grouped = df.groupby('Periodo')['I1R1C1N'].value_counts(normalize=True).unstack() * 100
    df_grouped = df_grouped.rename(columns={1: 'Sí', 2: 'No'}).reset_index()

    # Redondear los valores al primer decimal para evitar decimales extra
    df_grouped = df_grouped.round(1)

    # Transformar datos a formato largo para Plotly
    df_melted = df_grouped.melt(id_vars='Periodo', var_name='Introdujo Innovación', value_name='Porcentaje')

    # Definir colores personalizados
    colores_innovacion = {
        "Sí": "#a50026",  # Rojo oscuro
        "No": "#3b4cc0"   # Azul oscuro
    }

    # Crear gráfico de barras apiladas
    fig = px.bar(df_melted,
                x="Periodo",
                y="Porcentaje",
                color="Introdujo Innovación",
                text=df_melted["Porcentaje"],  # Asegurar que se usen valores redondeados
                color_discrete_map=colores_innovacion,
                title="Porcentaje de empresas con bienes o servicios nuevos por periodo.",
                labels={"Periodo": "Periodo", "Porcentaje": "Porcentaje (%)"},
                barmode="relative"
    )

    # Ajustar apariencia del gráfico
    fig.update_traces(
        texttemplate='%{y:.1f}%' ,  # Muestra valores con un decimal seguido de '%'
        textposition='inside',  # Asegura que el texto esté dentro de la barra
        insidetextanchor="end",  # Centra el texto dentro de la barra
        textfont_size=20, # Aumenta el tamaño del texto
        cliponaxis=False  # Evita que Plotly recorte textos en barras pequeñas
    )

    fig.update_layout(
        yaxis=dict(title="Porcentaje", tickformat=".0f"),  # Formato sin decimales en el eje Y
        xaxis=dict(title="Periodo"),
        legend_title="Introdujo Innovación"
    )

    # Mostrar gráfico en Streamlit
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
        textposition='inside',
        textfont=dict(size=22), 
        cliponaxis=False, # Las etiquetas estarán dentro de las barras
    ))
    fig.add_trace(go.Bar(
        x=df_innovacion.index,
        y=df_innovacion['No'],
        name='No',
        marker_color='#3b4cc0',  # Color personalizado (puedes cambiarlo)
        text=df_innovacion['No'],  # Etiquetas de los valores
        textposition='inside',
        insidetextanchor="end",
        textfont=dict(size=22),
        cliponaxis=False, #Las etiquetas estarán dentro de las barras
    ))

    # Personalizar la disposición del gráfico
    fig.update_layout(
        title='Total de empresas con bienes y servicios nuevos por periodo',
        xaxis_title='Periodo',
        yaxis_title='Cantidad de Empresas',
        barmode='stack',  # Apilamos las barras
        xaxis={'tickmode': 'array', 'tickvals': df_innovacion.index, 'ticktext': df_innovacion.index},  # Aseguramos que las etiquetas en el eje x sean correctas
        legend_title='¿Innovación en el Mercado?',
        template='plotly_dark'  # Opcional: Puedes cambiar el tema de colores
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    st.write("### Estadísticos:")
    est=estadisticos('I1R1C1N')
    st.dataframe(est)

elif selected == "2. N° promedio de bienes/servicios nuevos por periodo.":
    st.title("I1R1C2N:Número de servicios y/o bienes nuevos de la empresa introducidos en el mercado nacional en el período.")
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
        textposition='inside',
        insidetextanchor="end",
        textfont=dict(size=22),
        cliponaxis=False # Las etiquetas estarán fuera de las barras
    ))

    # Personalización del gráfico
    fig.update_layout(
        title='Promedio de bienes/servicios nuevos por periodo.',
        xaxis_title='Periodo',
        yaxis_title='Promedio',
        showlegend=False,  # No mostrar la leyenda ya que solo hay una serie
        font=dict(size=22),
    )

    # Mostrar el gráfico
    st.plotly_chart(fig)
    st.write("### Estadísticos:")
    est=estadisticos('I1R1C2N')
    st.dataframe(est)
elif selected == "3.Número total de innovaciones por periodo.":
    st.title("I1R4C2N:Número total de innovaciones de servicios o bienes nuevos por periodo.")
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
        textposition='inside',
        insidetextanchor="end",
        textfont=dict(size=22),
        cliponaxis=False # Las etiquetas estarán fuera de las barras
    ))

    # Personalización del gráfico
    fig.update_layout(
        title='Total de innovaciones de bienes/servicios nuevos por periodo.',
        xaxis_title='Periodo',
        yaxis_title='Cantidad total de innovaciones',
        showlegend=False,  # No mostrar la leyenda ya que solo hay una serie
        font=dict(size=20),
        
    )

    # Mostrar el gráfico
    st.plotly_chart(fig)

    st.write("### Estadísticos:")
    est=estadisticos('I1R4C2N')
    st.dataframe(est)
elif selected == "4.Innovación por actividad económica por periodo.":
    st.title("CIIU4:Actividad económica.")
        
    # Agrupar los datos por 'Actividad económica' y 'Periodo' y contar las ocurrencias
    count_data = df_emp.groupby(['Actividad económica', 'Periodo']).size().reset_index(name='Número de empresas')

    # Crear el gráfico de barras transpuesto
    fig = px.bar(count_data,
                x='Actividad económica',  # Ahora 'Actividad económica' está en el eje X
                y='Número de empresas',   # Y 'Número de empresas' va al eje Y
                color='Periodo',
                orientation='v',  # Cambiamos la orientación a vertical
                category_orders={'Actividad económica': df_emp['Actividad económica'].value_counts().index},
                title='Distribución de empresas que innovan por actividad económica y periodo.',
                labels={'Número de empresas': 'Número de empresas', 'Actividad económica': 'Actividad Económica'},
                color_continuous_scale='coolwarm')

    # Agregar las etiquetas de los valores
    fig.update_traces(texttemplate='%{y}', textposition='outside', insidetextanchor='start',textfont=dict(size=22),cliponaxis=False)

    # Configurar la leyenda
    fig.update_layout(
        title="Distribución de empresas que innovan por actividad económica y periodo.",
        xaxis_title='Actividad Económica',
        yaxis_title='Número de empresas',
        legend_title='Periodo',
        barmode='stack',
        xaxis=dict(
            tickfont=dict(size=14)  # Aumenta el tamaño de las etiquetas en el eje X
        ),
        yaxis=dict(
            tickfont=dict(size=14)  # Aumenta el tamaño de las etiquetas en el eje Y
        ),
        height=1000,  # Aumentamos la altura de la gráfica
        bargap=0.1  # Reducimos el espacio entre las barras
    )

    # Mostrar la gráfica
    st.plotly_chart(fig)
elif selected == "5.Empresas que innovan por tipología y periodo.":
    st.title("TIPOLO:Tipología (Amplia, Estricta, Potencial, Intencional, No Innovadora)")
    # Agrupar los datos por 'TIPOLO' y 'Periodo' y contar las ocurrencias
    count_data = df.groupby(['TIPOLO', 'Periodo']).size().reset_index(name='Número de empresas')

    # Crear el gráfico de barras invertido (de horizontal a vertical)
    fig = px.bar(count_data,
                x='TIPOLO',  # Ahora 'TIPOLO' está en el eje X
                y='Número de empresas',   # Y 'Número de empresas' va al eje Y
                color='Periodo',
                orientation='v',  # Cambiar la orientación a vertical
                category_orders={'TIPOLO': df['TIPOLO'].value_counts().index},
                title='Distribución de empresas por tipología y periodo.',
                labels={'Número de empresas': 'Número de empresas', 'TIPOLO': 'Tipología'},
                color_continuous_scale='coolwarm')

    # Agregar las etiquetas de los valores
    fig.update_traces(texttemplate='%{y}', textposition='outside', insidetextanchor='start',textfont=dict(size=22),cliponaxis=False)

    # Configurar la leyenda y el tamaño
    fig.update_layout(
        title='Distribución de empresas por tipología y periodo.',
        xaxis_title='Tipología',
        yaxis_title='Número de empresas',
        legend_title='Periodo',
        barmode='stack',
        xaxis=dict(
            tickfont=dict(size=18)  # Aumenta el tamaño de las etiquetas en el eje X
        ),
        yaxis=dict(
            tickfont=dict(size=18)  # Aumenta el tamaño de las etiquetas en el eje Y
        ),
        height=600,  # Aumenta la altura del gráfico para hacerlo más grande
        width=1000  # Aumenta el ancho del gráfico si es necesario
    )

    # Mostrar la gráfica
    st.plotly_chart(fig)
elif selected == "6.Empresas con bienes mejorados.":
    st.title("I1R1C1M:Servicios o bienes mejorados para su empresa. Si=1, No=2")
    # Calcular el porcentaje de empresas con bienes/servicios mejorados por periodo
    bienes_mejorados = df.groupby('Periodo')['I1R1C1M'].value_counts(normalize=True).unstack() * 100
    # Rellenar los valores faltantes con 0 (si alguna categoría no está presente para algún periodo)
    bienes_mejorados = bienes_mejorados.fillna(0)

    # Renombrar las columnas para que sean más comprensibles
    bienes_mejorados = bienes_mejorados.rename(columns={1: 'Sí', 2: 'No'})  # Asegúrate de que estos valores coincidan con tu dataset

    # Resetear el índice para convertir 'Periodo' en una columna regular
    bienes_mejorados = bienes_mejorados.reset_index()

    # Crear el gráfico de barras apiladas con Plotly
    fig = px.bar(bienes_mejorados, x='Periodo', y=['Sí', 'No'], 
                title='Porcentaje de empresas con bienes/servicios mejorados por periodo.',
                labels={'Periodo': 'Año', 'value': 'Porcentaje', 'variable': 'Bienes/Servicios mejorados'},
                color='variable', 
                color_discrete_sequence=["#a50026", "#3b4cc0"],
                text_auto=True)

    # Agregar etiquetas de porcentaje a las barras
    fig.update_traces(texttemplate='%{value:.1f}%', textposition='inside', hoverinfo='text',insidetextanchor='end',textfont=dict(size=22),cliponaxis=False)

    # Mostrar el gráfico interactivo en Streamlit
    st.plotly_chart(fig)
    st.write("### Estadísticos:")
    est=estadisticos('I1R1C1M')
    st.dataframe(est)
elif selected == "7.Impacto en la innvación.":
    st.title("Impacto en la innvocación.")   
    st.write("- **I2R5C1:** Aumento de la productividad.")
    st.write("- **I2R6C1:** Reducción de los costos laborales.")
    st.write("- **I2R7C1:** Reducción en el uso de materias primas o insumos.")
    st.write("- **I2R8C1:** Reducción en el consumo de energía u otros energéticos.")
    st.write("- **I2R9C1:** Reducción en el consumo de agua.")
    st.write("- **I2R10C1:** Reducción en costos asociados a comunicaciones.")
    st.write("- **I2R11C1:** Reducción en costos asociados a transporte.")
    st.write("- **I2R12C1:** Reducción en costos de mantenimiento y reparaciones.")
    # Cargar los datos con low_memory=False para evitar advertencias
    file_paths = {
        "2016-2017": '/workspaces/Prueba/EDIT_S_VI_2016_2017.csv',
        "2018-2019": '/workspaces/Prueba/EDITS_VII_2018_2019.csv',
        "2020-2021": '/workspaces/Prueba/Estructura_EDITS_VIII_2020_2021.csv'
    }

    dataframes = {}
    for period, path in file_paths.items():
        dataframes[period] = pd.read_csv(path, sep=';', low_memory=False)

    # Diccionario de categorías
    category_labels = {1: "Alta", 2: "Media", 3: "Nula", 4: "Negativo"}
    impact_columns = ["I2R5C1", "I2R6C1", "I2R7C1", "I2R8C1", "I2R9C1", "I2R10C1", "I2R11C1", "I2R12C1"]
    impact_labels = {
        "I2R5C1": "Aumento de la productividad",
        "I2R6C1": "Reducción de los costos laborales",
        "I2R7C1": "Reducción en el uso de materias primas o insumos",
        "I2R8C1": "Reducción en el consumo de energía u otros energéticos",
        "I2R9C1": "Reducción en el consumo de agua",
        "I2R10C1": "Reducción en costos asociados a comunicaciones",
        "I2R11C1": "Reducción en costos asociados a transporte",
        "I2R12C1": "Reducción en costos de mantenimiento y reparaciones"
    }

    # Convertir las columnas de impacto a numéricas
    for period, df in dataframes.items():
        for col in impact_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Función para obtener proporciones de cada categoría
    def get_category_proportions(df, columns):
        proportions = {category: [] for category in category_labels.values()}

        for col in columns:
            counts = df[col].value_counts(normalize=True).reindex([1, 2, 3, 4], fill_value=0)
            for cat_num, cat_label in category_labels.items():
                proportions[cat_label].append(counts[cat_num])

        return proportions

    # Obtener proporciones para cada año
    proportions = {period: get_category_proportions(df, impact_columns) for period, df in dataframes.items()}

    # Diccionario de colores por categoría y período
    colors = {
        ("Alta", "2016-2017"): "#2E7D32", ("Alta", "2018-2019"): "#66BB6A", ("Alta", "2020-2021"): "#A5D6A7",
        ("Media", "2016-2017"): "#FF8F00", ("Media", "2018-2019"): "#FFB300", ("Media", "2020-2021"): "#FFD54F",
        ("Nula", "2016-2017"): "#D84315", ("Nula", "2018-2019"): "#FF7043", ("Nula", "2020-2021"): "#FFAB91",
        ("Negativo", "2016-2017"): "#6A1B9A", ("Negativo", "2018-2019"): "#AB47BC", ("Negativo", "2020-2021"): "#CE93D8"
    }
    # Crear la figura
    fig = go.Figure()

    # Ancho de barras
    bar_width = 0.25
    x = np.arange(len(impact_columns))  # Posiciones en X

    # Agregar barras apiladas para cada período
    for i, (period, prop) in enumerate(proportions.items()):
        bottom = np.zeros(len(impact_columns))
        for category in category_labels.values():
            values = prop[category]
            fig.add_trace(go.Bar(
                x=[impact_labels[col] for col in impact_columns],
                y=values,
                name=f"{category} ({period})",
                marker_color=colors[(category, period)],
                offsetgroup=i,
                base=bottom,
                text=[f"{v * 100:.1f}%" for v in values],  # Convertir valores a porcentaje
                textposition="inside",  # Ubicar texto dentro de las barras
                textfont=dict(size=14, color="white"),
            ))
            bottom += values

    # Configuración del diseño
    title_text = "Distribución de impacto de innovación por ítem y período"
    fig.update_layout(
    barmode='stack',
    title=title_text,
    xaxis=dict(
        tickangle=-45,
        title=dict(text="Ítems de impacto", font=dict(size=20)),  # Aumentar tamaño del título del eje X
        tickfont=dict(size=16)  # Aumentar tamaño de los valores del eje X
    ),
    yaxis=dict(
        tickformat=".0%",
        title=dict(text="Proporción de respuestas", font=dict(size=20)),  # Aumentar tamaño del título del eje Y
        tickfont=dict(size=16)  # Aumentar tamaño de los valores del eje Y
    ),
    legend_title="Categoría de impacto",
    bargap=0.2,
    width=1500,
    height=800
)

    st.plotly_chart(fig)
if selected=="8.Empresas que introdujeron un bien o servicio unicamente en el mercado internacional.":
    st.title("I1R2C1N:Servicios o bienes nuevos en el mercado nacional (Ya existían en el mercado internacional). Si=1, No=2")
        # Crear la figura con 3 subgráficos
    fig = make_subplots(
    rows=1, cols=3, 
    specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]],
    subplot_titles=['<br>2016-2017', '<br>2018-2019', '<br>2020-2021']  # Añadir <br> para bajar los títulos
    )
    # Lista de dataframes y títulos
    dataframes = [df_2016, df_2018, df_2020]

    # Colores
    colors = ['#ff9999', '#66b3ff']

    # Generar las gráficas de pastel en los subgráficos
    for i, df in enumerate(dataframes):
        nuevos_counts = df['I1R2C1N'].value_counts(normalize=True) * 100
        labels = ['No', 'Sí']
        
        fig.add_trace(go.Pie(
        labels=labels,
        values=nuevos_counts,
        hole=0.3,  # Opción para hacer un gráfico tipo "donut"
        marker=dict(colors=colors),
        textinfo='percent+label',
        textfont=dict(size=20),  # Aumenta el tamaño de las etiquetas
        insidetextfont=dict(size=20)  # Asegura que el texto dentro del gráfico también sea grande
        ), row=1, col=i+1)


    fig.update_layout(
    title_text="Porcentaje de empresas que introdujeron bienes o servicios nuevos",
    title_x=0.5,  # Centrado horizontalmente
    title_y=0.95,  # Bajarlo un poco
    title_font=dict(size=20),  # Aumentar tamaño del título
    title_pad=dict(b=30),  # Agregar más espacio entre el título y la gráfica
    showlegend=False,
    width=1000,
    height=500,
    annotations=[
        dict(
            text="2016-2017", x=0.13, y=1.08, xref="paper", yref="paper", showarrow=False, font=dict(size=16)
        ),
        dict(
            text="2018-2019", x=0.50, y=1.08, xref="paper", yref="paper", showarrow=False, font=dict(size=16)
        ),
        dict(
            text="2020-2021", x=0.87, y=1.08, xref="paper", yref="paper", showarrow=False, font=dict(size=16)
        )
    ]
    )
    # Mostrar figura en Streamlit
    st.plotly_chart(fig)
    
if selected=="9.Impacto en la innovación de las empresas de servicios.":
    # Título de la aplicación en Streamlit
    st.title("Distribución de Indicadores de Impacto")
    st.write("### Definiciones:")
    st.write("- **I2R3C1:** Mantenido Participación.")
    st.write("- **I2R4C1:** Ingresado Nuevo Mercado.")
    st.write("- **I2R16C1:** Aumento Ventas.")
    st.write("- **I2R17C1:** Ha mantenido su participación en el mercado geográfico de su empresa.")

    # Cargar datasets
    df_2018_2019 = pd.read_csv("/workspaces/Prueba/EDITS_VII_2018_2019.csv", sep=';', low_memory=False)
    df_2020_2021 = pd.read_csv("/workspaces/Prueba/Estructura_EDITS_VIII_2020_2021.csv", sep=';', low_memory=False)

    # Seleccionar solo las columnas relevantes
    columnas_seleccionadas = ["I2R3C1", "I2R4C1", "I2R16C1", "I2R17C1"]
    df_2018_2019 = df_2018_2019[columnas_seleccionadas]
    df_2020_2021 = df_2020_2021[columnas_seleccionadas]

    # Agregar columna de periodo
    df_2018_2019["Periodo"] = "2018-2019"
    df_2020_2021["Periodo"] = "2020-2021"

    # Unir los datasets
    df_total = pd.concat([df_2018_2019, df_2020_2021])

    # Renombrar las columnas con descripciones más claras
    df_total = df_total.rename(columns={
        "I2R3C1": "Mantenido Participación",
        "I2R4C1": "Ingresado Nuevo Mercado",
        "I2R16C1": "Aumento Ventas",
        "I2R17C1": "Mantenido Participación 2"
    })

    # Transformar a formato largo
    df_melted = df_total.melt(id_vars=["Periodo"], var_name="Indicador", value_name="Nivel")

    # Convertir "Nivel" a numérico y eliminar valores no válidos
    df_melted["Nivel"] = pd.to_numeric(df_melted["Nivel"], errors='coerce')
    df_melted = df_melted.dropna(subset=["Nivel"])

    # Mapear valores a sus categorías correctas
    niveles_map = {1: "Alta", 2: "Media", 3: "Nula", 4: "Impacto Negativo"}
    df_melted["Nivel"] = df_melted["Nivel"].map(niveles_map)

    # Definir colores personalizados
    # Definir colores personalizados
    colores_niveles = {
        "Alta": "#1B5E20",  # Verde oscuro
        "Media": "#64B5F6",  # Azul claro
        "Nula": "#9E9E9E",  # Gris
        "Impacto Negativo": "#B71C1C"  # Rojo oscuro
    }
    # 📊 Gráfica para **2018-2019**
    df_2018_2019_melted = df_melted[df_melted["Periodo"] == "2018-2019"]

    fig1 = px.histogram(df_2018_2019_melted, 
                        x="Indicador", 
                        color="Nivel", 
                        barmode="group",  # Equivalente a "dodge" en Seaborn
                        text_auto=True,   # Mostrar valores en las barras
                        category_orders={"Indicador": df_melted["Indicador"].unique()},
                        color_discrete_map=colores_niveles)

    fig1.update_layout(
        title="Distribución de Indicadores de Impacto - 2018-2019",
        xaxis_title="Indicadores de Impacto",
        yaxis_title="Número de Empresas",
        bargap=0.2,
        legend_title="Nivel de Impacto"
    )

    # Mostrar en Streamlit
    st.plotly_chart(fig1)


    # 📊 Gráfica para **2020-2021**
    df_2020_2021_melted = df_melted[df_melted["Periodo"] == "2020-2021"]

    fig2 = px.histogram(df_2020_2021_melted, 
                        x="Indicador", 
                        color="Nivel", 
                        barmode="group", 
                        text_auto=True,
                        category_orders={"Indicador": df_melted["Indicador"].unique()},
                        color_discrete_map=colores_niveles)

    fig2.update_layout(
        title="Distribución de Indicadores de Impacto - 2020-2021",
        xaxis_title="Indicadores de Impacto",
        yaxis_title="Número de Empresas",
        bargap=0.2,
        legend_title="Nivel de Impacto"
    )

    # Mostrar en Streamlit
    st.plotly_chart(fig2)
