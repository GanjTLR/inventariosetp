import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
import io
import zipfile

def generar_documentos(df, word_template, prefijo, fecha_seleccionada):
    try:
        # Filtrar el DataFrame por la fecha seleccionada
        df_filtrado = df[df.iloc[:, 4].dt.date == fecha_seleccionada]
        
        if df_filtrado.empty:
            st.warning("⚠️ No hay registros para la fecha seleccionada.")
            return {}
        
        doc_template = DocxTemplate(word_template)
        archivos_generados = {}
        
        for _, row in df_filtrado.iterrows():
            doc = doc_template
            context = {
                "INTERNO": row.iloc[7],
                "PLACA": row.iloc[6],
                "FECHA": row.iloc[5].strftime('%Y-%m-%d'),
                "IP": row.iloc[8],
                "CODIGO": row.iloc[9],
                "TECNOLOGIA": row.iloc[11],
                "BOTÓNDEPÁNICO": row.iloc[12],
                "VALIDADORDETARJETASSETP": row.iloc[13],
                "VALIDADOREMV": row.iloc[15],
                "CÁMARA": row.iloc[14],
                "BARRASCONTADORES": row.iloc[16],
                "NUEVOSOPORTEANTI": row.iloc[19],
                "TABLET": row.iloc[18],
                "INHANDVG710": row.iloc[20],
                "POWERBANK": row.iloc[21],
                "BATERÍAINTERNA": row.iloc[22],
                "PROTECCIONESELÉCTRICAS": row.iloc[23],
            }
            
            doc.render(context)
            file_stream = io.BytesIO()
            doc.save(file_stream)
            file_stream.seek(0)
            archivos_generados[f"{prefijo}-{row.iloc[6]}.docx"] = file_stream
        
        return archivos_generados
    except Exception as e:
        st.error(f"Error al generar documentos: {e}")
        return {}

def crear_zip(archivos):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for nombre, archivo in archivos.items():
            zip_file.writestr(nombre, archivo.getvalue())
    zip_buffer.seek(0)
    return zip_buffer

def mostrar_generador_fichas():
    st.markdown("## 📄 Generador de Documentos Word")
    st.divider()
    
    df = st.session_state.get("df")
    
    if df is None or df.shape[1] < 5:
        st.error("❌ No se han cargado datos. Ve al Dashboard y actualiza.")
        return
    
    word_template = st.file_uploader("📂 Selecciona la plantilla Word", type=["docx"])
    prefijo = st.text_input("📝 Ingresa un prefijo para los archivos")
    
    # Selección de fecha
    df.iloc[:, 4] = pd.to_datetime(df.iloc[:, 4], errors='coerce')
    fechas_disponibles = sorted(df.iloc[:, 4].dropna().dt.date.unique())
    fecha_seleccionada = st.selectbox("📅 Selecciona la fecha de revisión", fechas_disponibles)
    
    if st.button("Generar Documentos y Descargar ZIP"):
        if word_template and prefijo:
            archivos = generar_documentos(df, word_template, prefijo, fecha_seleccionada)
            
            if archivos:
                st.success("✅ Documentos generados exitosamente. Descarga el archivo ZIP abajo.")
                
                # Descargar todo en ZIP
                zip_buffer = crear_zip(archivos)
                st.download_button(label="📥 Descargar Todo en ZIP", data=zip_buffer, file_name=f"{prefijo}_documentos.zip", mime="application/zip")
        else:
            st.warning("⚠️ Por favor, selecciona la plantilla Word e ingresa un prefijo antes de generar.")



