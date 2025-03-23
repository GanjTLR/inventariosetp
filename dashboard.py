import streamlit as st
import pandas as pd
import plotly.express as px

# Función para mostrar el dashboard
def mostrar_dashboard(df, columna_fecha):
    st.write("### Resumen y Gráficos Principales")
    col1, col2, col3 = st.columns(3)
    
    # Agrupar por fecha y contar revisiones
    df_resumen = df[columna_fecha].dt.date.value_counts().reset_index()
    df_resumen.columns = ["Fecha", "Cantidad de Buses Revisados"]
    df_resumen = df_resumen.sort_values("Fecha")
    
    # Resumen de revisiones en la primera columna
    with col1:
        st.write("#### Resumen de Revisiones")
        st.dataframe(df_resumen, height=400)  # Altura ajustada
    
    # Gráfico de barras en la segunda columna
    with col2:
        fig_bar = px.bar(df_resumen, x="Fecha", y="Cantidad de Buses Revisados", 
                         title="Buses Revisados por Día", text_auto=True)
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_chart")
    
    # Gráfico de pastel en la tercera columna
    with col3:
        st.write("#### Tecnología Conectada")
        
        # Contar la cantidad de "Sí" y "No" en la columna 11
        conteo_conectados = df[df.columns[11]].value_counts().reset_index()
        conteo_conectados.columns = ["Respuesta", "Cantidad"]
        
        # Crear el gráfico de pastel
        fig_pie = px.pie(conteo_conectados, values="Cantidad", names="Respuesta", 
                         title="Distribución de Tecnología Conectada")
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_conectados")
    
    # Botón para descargar resumen
    st.download_button(
        label="Descargar Resumen",
        data=df_resumen.to_csv(index=False).encode("utf-8"),
        file_name="resumen_revisiones.csv",
        mime="text/csv",
    )
    
    # Selección de gráficos en una fila
    st.write("### Selección de Gráficos Adicionales")
    col4, col5, col6 = st.columns(3)
    
    # Obtener las columnas desde K hasta W
    columnas_disponibles = df.columns[12:23]  # Columnas K a W (índices 11 a 23)
    
    # Selección de columnas para los gráficos
    with col4:
        columna_grafico1 = st.selectbox("Columna para Gráfico 1", columnas_disponibles, key="col1")
        tipo_grafico1 = st.selectbox("Tipo de gráfico para Gráfico 1", ["Barra", "Pastel"], key="tipo1")
    with col5:
        columna_grafico2 = st.selectbox("Columna para Gráfico 2", columnas_disponibles, key="col2")
        tipo_grafico2 = st.selectbox("Tipo de gráfico para Gráfico 2", ["Barra", "Pastel"], key="tipo2")
    with col6:
        columna_grafico3 = st.selectbox("Columna para Gráfico 3", columnas_disponibles, key="col3")
        tipo_grafico3 = st.selectbox("Tipo de gráfico para Gráfico 3", ["Barra", "Pastel"], key="tipo3")
    
    # Segunda fila: Tres gráficos adicionales
    col7, col8, col9 = st.columns(3)
    
    # Función para contar "Sí" y "No"
    def contar_si_no(columna):
        conteo = df[columna].value_counts().reset_index()
        conteo.columns = ["Respuesta", "Cantidad"]
        return conteo
    
    # Función para crear gráficos
    def crear_grafico(datos, columna, tipo):
        if tipo == "Barra":
            fig = px.bar(datos, x="Respuesta", y="Cantidad", 
                         title=f"Distribución de {columna}", text_auto=True)
        elif tipo == "Pastel":
            fig = px.pie(datos, values="Cantidad", names="Respuesta", 
                         title=f"Distribución de {columna}")
        return fig
    
    # Gráfico 1 en la primera columna
    with col7:
        st.write(f"#### Gráfico 1: {columna_grafico1}")
        datos_grafico1 = contar_si_no(columna_grafico1)
        fig1 = crear_grafico(datos_grafico1, columna_grafico1, tipo_grafico1)
        st.plotly_chart(fig1, use_container_width=True, key="grafico1")
    
    # Gráfico 2 en la segunda columna
    with col8:
        st.write(f"#### Gráfico 2: {columna_grafico2}")
        datos_grafico2 = contar_si_no(columna_grafico2)
        fig2 = crear_grafico(datos_grafico2, columna_grafico2, tipo_grafico2)
        st.plotly_chart(fig2, use_container_width=True, key="grafico2")
    
    # Gráfico 3 en la tercera columna
    with col9:
        st.write(f"#### Gráfico 3: {columna_grafico3}")
        datos_grafico3 = contar_si_no(columna_grafico3)
        fig3 = crear_grafico(datos_grafico3, columna_grafico3, tipo_grafico3)
        st.plotly_chart(fig3, use_container_width=True, key="grafico3")