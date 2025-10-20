import streamlit as st
import pandas as pd

# Configuración de la página - ocultar barra lateral
st.set_page_config(
    page_title="Visualizador de Datos Institucionales", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Ocultar elementos de la barra lateral usando CSS
hide_sidebar_style = """
    <style>
        /* Ocultar completamente la barra lateral */
        section[data-testid="stSidebar"] {
            display: none;
        }
        
        /* Asegurar que el contenido principal ocupe todo el ancho */
        .main .block-container {
            max-width: 100%;
            padding-left: 1rem;
            padding-right: 1rem;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Título principal
st.title("VISUALIZADOR DE DATOS INSTITUCIONALES")
st.caption("Última actualización: 20 de octubre de 2025")

# Cargar datos desde el archivo CSV con separador ;
try:
    df = pd.read_csv("tab0.csv", sep=';', encoding='utf-8')
    
    # Verificar que las columnas necesarias existan en el DataFrame
    required_columns = ['cat_periodo', 'tipo_inst_3', 'cod_inst', 'nomb_inst', 'rector_inst', 'estado']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"El archivo CSV no tiene las columnas requeridas. Faltan: {missing_columns}")
        st.stop()
        
except FileNotFoundError:
    st.error("No se encontró el archivo 'tab0.csv'. Asegúrate de que esté en el mismo directorio.")
    st.stop()
except Exception as e:
    st.error(f"Error al cargar el archivo CSV: {e}")
    
    # Intentar con diferentes encodings si hay problemas
    st.info("Intentando cargar con encoding alternativo...")
    try:
        df = pd.read_csv("tab0.csv", sep=';', encoding='latin-1')
        st.success("¡Archivo cargado exitosamente con encoding latin-1!")
        
        # Verificar columnas después de cargar con encoding alternativo
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"El archivo CSV no tiene las columnas requeridas. Faltan: {missing_columns}")
            st.stop()
            
    except Exception as e2:
        st.error(f"Error también con encoding alternativo: {e2}")
        st.stop()

# Selector de institución
selected_institution = st.selectbox(
    "🔍 Institución",
    options=df['nomb_inst'].unique(),
    key="institution_selector"
)

# Obtener código y datos de la institución seleccionada
selected_data = df[df['nomb_inst'] == selected_institution].iloc[0]
cod_inst = selected_data['cod_inst']

# Mostrar información institucional
st.divider()
st.header("CARACTERIZACIÓN INSTITUCIONAL")

col1, col2 = st.columns(2)

with col1:
    st.text_input("Institución", value=selected_data['nomb_inst'], disabled=True)
    st.text_input("Tipo de Institución", value=selected_data['tipo_inst_3'], disabled=True)

with col2:
    st.text_input("Estado", value=selected_data['estado'], disabled=True)
    st.text_input("Rector/a", value=selected_data['rector_inst'], disabled=True)

# Mostrar código institucional (oculto al usuario pero disponible para uso interno)
st.session_state['selected_institution_code'] = cod_inst
