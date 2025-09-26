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
    try:
        # Intentar diferentes configuraciones para el CSV
        # Opción 1: UTF-8
        try:
            data = pd.read_csv('Listado IES.csv', encoding='utf-8')
            st.success("Archivo cargado con encoding UTF-8")
            return data
        except:
            # Opción 2: Latin-1 (común en archivos de Windows)
            try:
                data = pd.read_csv('Listado IES.csv', encoding='latin-1')
                st.success("Archivo cargado con encoding Latin-1")
                return data
            except:
                # Opción 3: Con parámetros adicionales
                try:
                    data = pd.read_csv(
                        'Listado IES.csv', 
                        encoding='latin-1',
                        delimiter=',',
                        quotechar='"',
                        skipinitialspace=True,
                        engine='python',
                        on_bad_lines='skip'  # Saltar líneas problemáticas
                    )
                    st.success("Archivo cargado con parámetros extendidos")
                    return data
                except Exception as e:
                    st.error(f"No se pudo cargar el archivo: {str(e)}")
                    return pd.DataFrame()
    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")
        return pd.DataFrame()

data = load_data()

# Verificar si se cargaron datos
if data.empty:
    st.error("No se pudieron cargar los datos. Verifica el archivo CSV.")
    st.stop()

# Mostrar información básica del dataset
st.write(f"Dataset cargado: {len(data)} filas, {len(data.columns)} columnas")
st.write("Primeras filas del dataset:")
st.dataframe(data.head())

# Verificar que existe la columna 'ins_nom'
if 'ins_nom' not in data.columns:
    st.error("La columna 'ins_nom' no existe en el dataset. Columnas disponibles:")
    st.write(data.columns.tolist())
    st.stop()

# Obtener la lista de instituciones únicas a partir de la columna 'ins_nom'
instituciones = data['ins_nom'].unique().tolist()

# Ordenar alfabéticamente
instituciones.sort()

# Sidebar para mejor organización
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
                "Institución:",
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
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'ins_cod' in datos_institucion.columns:
            st.metric("Código Institución", datos_institucion['ins_cod'].iloc[0])
    
    with col2:
        if 'rec_nom' in datos_institucion.columns:
            st.metric("Rector/a", datos_institucion['rec_nom'].iloc[0])
    
    with col3:
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
else:
    st.warning("No se encontraron datos para la institución seleccionada")
