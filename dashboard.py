import streamlit as st
import pandas as pd
import plotly.express as px

# Función para mostrar el dashboard con mejor diseño
def mostrar_dashboard(df, columna_fecha):
    st.markdown("## 📊 Dashboard de Revisiones")
    st.divider()
    
    # Contenedor de resumen
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        # Agrupar por fecha y contar revisiones
        df_resumen = df[columna_fecha].dt.date.value_counts().reset_index()
        df_resumen.columns = ["Fecha", "Cantidad de Buses Revisados"]
        df_resumen = df_resumen.sort_values("Fecha")
        
        # Tabla de revisiones
        with col1:
            st.markdown("### 📅 Resumen de Revisiones")
            st.dataframe(df_resumen, height=400, use_container_width=True)
        
        # Gráfico de barras
        with col2:
            fig_bar = px.bar(df_resumen, x="Fecha", y="Cantidad de Buses Revisados", 
                             title="Buses Revisados por Día", text_auto=True, 
                             color_discrete_sequence=["#ADD8E6"])
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Gráfico de pastel
        with col3:
            st.markdown("### 🔗 Tecnología Conectada")
            conteo_conectados = df[df.columns[11]].value_counts().reset_index()
            conteo_conectados.columns = ["Respuesta", "Cantidad"]
            fig_pie = px.pie(conteo_conectados, values="Cantidad", names="Respuesta", 
                             title="Distribución de Tecnología Conectada",
                             color_discrete_sequence=["#87CEEB", "#4682B4"])
            st.plotly_chart(fig_pie, use_container_width=True)
    
    st.divider()
    
    # Botón de descarga
    st.download_button(
        label="📥 Descargar Resumen",
        data=df_resumen.to_csv(index=False).encode("utf-8"),
        file_name="resumen_revisiones.csv",
        mime="text/csv",
    )
    
    st.markdown("## 📈 Gráficos Adicionales")
    
    # Selección de gráficos
    col4, col5, col6 = st.columns(3)
    columnas_disponibles = df.columns[12:23]
    
    with col4:
        columna_grafico1 = st.selectbox("📌 Gráfico 1", columnas_disponibles, key="col1")
        tipo_grafico1 = st.radio("Tipo", ["Barra", "Pastel"], key="tipo1", horizontal=True)
    with col5:
        columna_grafico2 = st.selectbox("📌 Gráfico 2", columnas_disponibles, key="col2")
        tipo_grafico2 = st.radio("Tipo", ["Barra", "Pastel"], key="tipo2", horizontal=True)
    with col6:
        columna_grafico3 = st.selectbox("📌 Gráfico 3", columnas_disponibles, key="col3")
        tipo_grafico3 = st.radio("Tipo", ["Barra", "Pastel"], key="tipo3", horizontal=True)
    
    # Funciones auxiliares
    def contar_si_no(columna):
        conteo = df[columna].value_counts().reset_index()
        conteo.columns = ["Respuesta", "Cantidad"]
        return conteo
    
    def crear_grafico(datos, columna, tipo):
        if tipo == "Barra":
            fig = px.bar(datos, x="Respuesta", y="Cantidad", 
                         title=f"Distribución de {columna}", text_auto=True,
                         color_discrete_sequence=["#ADD8E6"])
        else:
            fig = px.pie(datos, values="Cantidad", names="Respuesta", 
                         title=f"Distribución de {columna}",
                         color_discrete_sequence=["#B0E0E6", "#4682B4"])
        return fig
    
    col7, col8, col9 = st.columns(3)
    
    columnas_seleccionadas = [columna_grafico1, columna_grafico2, columna_grafico3]
    tipos_seleccionados = [tipo_grafico1, tipo_grafico2, tipo_grafico3]
    columnas_unicas = set(columnas_seleccionadas)
    
    if len(columnas_unicas) < len(columnas_seleccionadas):
        st.warning("⚠️ Selecciona columnas diferentes para cada gráfico para evitar errores.")
    else:
        with col7:
            st.markdown(f"### 📊 {columna_grafico1}")
            fig1 = crear_grafico(contar_si_no(columna_grafico1), columna_grafico1, tipo_grafico1)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col8:
            st.markdown(f"### 📊 {columna_grafico2}")
            fig2 = crear_grafico(contar_si_no(columna_grafico2), columna_grafico2, tipo_grafico2)
            st.plotly_chart(fig2, use_container_width=True)
        
        with col9:
            st.markdown(f"### 📊 {columna_grafico3}")
            fig3 = crear_grafico(contar_si_no(columna_grafico3), columna_grafico3, tipo_grafico3)
            st.plotly_chart(fig3, use_container_width=True)