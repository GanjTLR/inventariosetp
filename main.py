import streamlit as st
import pandas as pd
import requests
import io
from dashboard import mostrar_dashboard
from vista_completa import mostrar_vista_completa

# Función para descargar un archivo de Google Drive
def descargar_archivo(file_id):
    url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
    response = requests.get(url)
    return io.BytesIO(response.content)

# Función para cargar datos desde Google Drive
def cargar_datos(file_id):
    # Descargar el archivo Excel
    archivo = descargar_archivo(file_id)
    
    # Leer el archivo Excel
    df = pd.read_excel(archivo, header=0)  # Usar la fila como encabezados
    
    
    # Asumir que la columna de fecha es la quinta columna (índice 4)
    columna_fecha = df.columns[5]  # La quinta columna (índice 4)
    
    # Convertir la columna de fecha a datetime y manejar errores
    df[columna_fecha] = pd.to_datetime(df[columna_fecha], errors='coerce')
    
    # Filtrar filas con fechas válidas (eliminar NaT)
    df = df.dropna(subset=[columna_fecha])
    
    return df, columna_fecha

# Función principal
def main():
    # Configuración de la página
    st.set_page_config(page_title="Dashboard de Datos", layout="wide")
    
    
    # Título del Dashboard
    st.title("📊  INVENTARIO TECNOLOGIA 🚌")
    
    # Inicializar el estado de la página
    if "pagina" not in st.session_state:
        st.session_state.pagina = "Dashboard"
    
    # Botón para Dashboard
    if st.sidebar.button(
        '📊 Dashboard',
        help="Ir al Dashboard",
        use_container_width=True,
    ):
        st.session_state.pagina = "Dashboard"
    
    # Botón para Vista Completa
    if st.sidebar.button(
        '📄 Vista Completa',
        help="Ir a la Vista Completa",
        use_container_width=True,
    ):
        st.session_state.pagina = "Vista Completa"
    
    # Botón para actualizar los datos
    if st.sidebar.button(
        '🔄 Actualizar Datos',
        help="Descargar el archivo actualizado desde Google Drive",
        use_container_width=True,
    ):
        st.session_state.datos_actualizados = False  # Forzar la actualización
    
    # ID del archivo en Google Drive
    file_id = "1UKZWpGcXV7mfVJgTiedy--Ok2TpAcxwBlk5sSVmqhoY"  # ID de tu archivo
    
    # Cargar datos
    try:
        if "datos_actualizados" not in st.session_state or not st.session_state.datos_actualizados:
            df, columna_fecha = cargar_datos(file_id)
            st.session_state.df = df
            st.session_state.columna_fecha = columna_fecha
            st.session_state.datos_actualizados = True
        else:
            df = st.session_state.df
            columna_fecha = st.session_state.columna_fecha
        
        if df is not None:
            if st.session_state.pagina == "Dashboard":
                mostrar_dashboard(df, columna_fecha)
            elif st.session_state.pagina == "Vista Completa":
                mostrar_vista_completa(df, columna_fecha)
        else:
            st.error("No se pudieron cargar los datos desde Google Drive.")
    except Exception as e:
        st.error(f"Error al descargar el archivo: {e}")

# Ejecutar la función principal
if __name__ == "__main__":
    main()
