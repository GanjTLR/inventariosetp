import streamlit as st
import pandas as pd
import requests
import io
from dashboard import mostrar_dashboard
from vista_completa import mostrar_vista_completa

def descargar_archivo(file_id):
    url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
    response = requests.get(url)
    return io.BytesIO(response.content)

def cargar_datos(file_id):
    archivo = descargar_archivo(file_id)
    df = pd.read_excel(archivo, header=0)
    columna_fecha = df.columns[5]  # Quinta columna (índice 4)
    df[columna_fecha] = pd.to_datetime(df[columna_fecha], errors='coerce')
    df = df.dropna(subset=[columna_fecha])
    return df, columna_fecha

def main():
    st.set_page_config(page_title="Dashboard de Datos", layout="wide")
    
    st.title("📊  INVENTARIO TECNOLOGIA 🚌")
    
    if "pagina" not in st.session_state:
        st.session_state.pagina = "Dashboard"
    
    with st.sidebar:
        st.markdown("## Navegación")
        st.markdown("---")
        if st.button('📊 Dashboard', use_container_width=True):
            st.session_state.pagina = "Dashboard"
        if st.button('📄 Vista Completa', use_container_width=True):
            st.session_state.pagina = "Vista Completa"
        if st.button('🔄 Actualizar Datos', use_container_width=True):
            st.session_state.datos_actualizados = False
    
    file_id = "1UKZWpGcXV7mfVJgTiedy--Ok2TpAcxwBlk5sSVmqhoY"
    
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

if __name__ == "__main__":
    main()
