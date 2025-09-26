# Paquetes utilizados
import streamlit as st
import pandas as pd
import numpy as np

## ESTABLECE CARACTERÍSTICAS GENERALES DEL SITIO
# Define título de la página
st.set_page_config(page_title="Visualizador CNED", layout="wide")

# Inserta el ícono del CNED en la parte superior derecha de la página
st.markdown(
    """
    <div style="text-align: right;">
        <img src="https://cned.cl/wp-content/uploads/2023/10/cned_s_fondo.png" width="100">
    </div>
    """,
    unsafe_allow_html=True
)

# Presentación del visualizador
st.title("**VISUALIZADOR DE DATOS INSTITUCIONALES**")
st.subheader("Última actualización: 30 de septiembre de 2025")
st.markdown("Contacto: Fabián Ramírez (framirez@cned.cl)")

## CARGA LA BASE DE DATOS DE INFORMACIÓN GENERAL
@st.cache_data
def load_data():
    # Carga directa con el separador conocido
    data = pd.read_csv('Listado IES.csv', sep=';', encoding='utf-8')
    return data

data = load_data()

# Obtener la lista de instituciones únicas a partir de la columna 'ins_nom'
instituciones = data['ins_nom'].unique().tolist()
instituciones.sort()

# Sidebar para selección de institución
with st.sidebar:
    st.header("🏫 Selección de Institución")
    
    # Buscador
    buscar = st.text_input("Buscar institución:", "")
    
    # Filtrar opciones si se usa el buscador
    if buscar:
        opciones_filtradas = [inst for inst in instituciones if buscar.lower() in inst.lower()]
        if opciones_filtradas:
            institucion_seleccionada = st.selectbox(
                "Resultados de búsqueda:",
                opciones_filtradas,
                key="selector_busqueda"
            )
        else:
            st.warning("No se encontraron instituciones con ese criterio.")
            institucion_seleccionada = st.selectbox(
                "Todas las instituciones:",
                instituciones,
                key="selector_institucion"
            )
    else:
        institucion_seleccionada = st.selectbox(
            "Institución:",
            instituciones,
            key="selector_institucion"
        )

# Filtrar los datos para la institución seleccionada
datos_institucion = data[data['ins_nom'] == institucion_seleccionada]

# Mostrar información de la institución seleccionada
if not datos_institucion.empty:
    st.success(f"✅ Institución seleccionada: **{institucion_seleccionada}**")
    
    # Mostrar información básica
    col1, col2 = st.columns(2)
    
    with col1:
        if 'rec_nom' in datos_institucion.columns:
            st.metric("Rector/a", datos_institucion['rec_nom'].iloc[0])
    
    with col2:
        if 'pro_cned' in datos_institucion.columns:
            st.metric("Proceso CNED", datos_institucion['pro_cned'].iloc[0])
    
    # Mostrar información del directorio si existe
    if any(col.startswith('dir') for col in datos_institucion.columns):
        st.subheader("👥 Directorio")
        directores = []
        for i in range(1, 10):  # Para dir1 a dir9
            nom_col = f'dir{i}_nom'
            rol_col = f'dir{i}_rol'
            pro_col = f'dir{i}_pro'
            
            if (nom_col in datos_institucion.columns and 
                pd.notna(datos_institucion[nom_col].iloc[0])):
                directores.append({
                    'nombre': datos_institucion[nom_col].iloc[0],
                    'rol': datos_institucion[rol_col].iloc[0] if rol_col in datos_institucion.columns else 'N/A',
                    'profesion': datos_institucion[pro_col].iloc[0] if pro_col in datos_institucion.columns else 'N/A'
                })
        
        for director in directores:
            st.write(f"**{director['nombre']}** - {director['rol']} ({director['profesion']})")
