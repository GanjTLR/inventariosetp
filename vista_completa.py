import streamlit as st
import pandas as pd
import datetime

# Función para mostrar la vista completa con mejor diseño
def mostrar_vista_completa(df, columna_fecha):
    st.markdown("## 🔍 Vista Completa de Datos")
    st.divider()
    
    # Obtener las fechas únicas en las que se realizó el inventario
    fechas_inventario = df[columna_fecha].dt.date.unique()
    
    # Organizar el espacio: título a la izquierda y calendario a la derecha
    col1, col2 = st.columns([3, 1])  # col1 más grande para el título, col2 para el calendario
    
    with col1:
        st.markdown("### 📋 Datos de Inventario")
    
    with col2:
        st.markdown("### 📅 Días con Inventario")
        st.markdown("\n".join(f"- **{fecha.strftime('%Y-%m-%d')}**" for fecha in sorted(fechas_inventario)))
    
    # Obtener la primera fecha disponible
    primera_fecha = df[columna_fecha].min().date()
    
    st.divider()
    
    # Buscador con mejor organización
    st.markdown("## 🔎 Búsqueda de Registros")
    col10, col11, col12 = st.columns(3)
    
    with col10:
        buscar_placa = st.text_input("🚗 Buscar por placa de vehículo")
    with col11:
        buscar_vehiculo = st.text_input("🚍 Buscar por número interno de vehículo")
    with col12:
        buscar_fecha = st.date_input("📆 Buscar por fecha", value=primera_fecha)
    
    # Filtrar el DataFrame según los criterios de búsqueda
    df_filtrado = df.copy()
    
    if buscar_placa:
        df_filtrado = df_filtrado[df_filtrado["Placa de vehículo."].astype(str).str.contains(buscar_placa, case=False, na=False)]
    if buscar_vehiculo:
        df_filtrado = df_filtrado[df_filtrado["Numero interno."].astype(str).str.contains(buscar_vehiculo, case=False, na=False)]
    if buscar_fecha:
        df_filtrado = df_filtrado[df_filtrado[columna_fecha].dt.date == buscar_fecha]
    else:
        df_filtrado = df_filtrado[df_filtrado[columna_fecha].dt.date >= primera_fecha]
    
    st.divider()
    
    # Mostrar el DataFrame filtrado con información
    st.markdown(f"### 📊 Resultados Encontrados: {len(df_filtrado)} registros")
    st.dataframe(df_filtrado, height=600, use_container_width=True)

# Ejemplo de uso
if __name__ == "__main__":
    # Crear un DataFrame de ejemplo
    data = {
        "Placa de vehículo.": ["ABC123", "XYZ789", "DEF456", "GHI789"],
        "Numero interno.": [101, 102, 103, 104],
        "Fecha de inventario": pd.to_datetime(["2023-10-01", "2023-10-02", "2023-10-15", "2023-10-20"])
    }
    df = pd.DataFrame(data)
    
    # Mostrar la vista completa
    mostrar_vista_completa(df, "Fecha de inventario")
