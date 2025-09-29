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

# Cargar datos desde CSV
@st.cache_data
def cargar_instituciones():
    # Aquí cargarías tu archivo con los 200 nombres
    return pd.read_csv('Listado IES.csv')

instituciones_df = cargar_instituciones()

institucion_seleccionada = st.selectbox(
        "Institución:",
        instituciones_df['nombre'].tolist(),
        key="selector_institucion"
    )

# Filtrar los datos para la institución seleccionada
datos_institucion = data[data['ins_nom'] == institucion_seleccionada]

# Mostrar información de la institución seleccionada
if not datos_institucion.empty:
    st.success(f"**{institucion_seleccionada}**")
    
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
