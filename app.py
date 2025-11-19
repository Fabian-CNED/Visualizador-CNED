import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página - ocultar barra lateral
st.set_page_config(
    page_title="Visualizador de Datos Institucionales", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Ocultar elementos de la barra lateral y footer usando CSS
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
        
        /* Ocultar el footer de Streamlit */
        footer {
            visibility: hidden;
        }
        
        /* Ocultar el menú hamburguesa en móviles */
        .st-emotion-cache-1dp5vir {
            display: none;
        }
        
        /* Ocultar elementos específicos del footer de Streamlit */
        .stAppFooter {
            display: none;
        }
        
        /* Ocultar el badge "Made with Streamlit" */
        .stAppFooter footer {
            display: none;
        }
        
        /* Ocultar cualquier elemento con la clase que contenga 'footer' */
        [data-testid="stFooter"] {
            display: none;
        }
        
        /* Ocultar elementos del footer en la vista principal */
        #MainMenu {
            visibility: hidden;
        }
        
        /* Asegurar que no haya espacio reservado para el footer */
        .stApp {
            bottom: 0;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Título principal
st.title("VISUALIZADOR DE DATOS INSTITUCIONALES")
st.caption("Última actualización: 20 de octubre de 2025")

# Cargar datos desde el archivo CSV
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
    st.text_input("Institución", value=selected_data['nomb_inst'])
    st.text_input("Tipo de Institución", value=selected_data['tipo_inst_3'])

with col2:
    st.text_input("Estado", value=selected_data['estado'])
    st.text_input("Rector/a", value=selected_data['rector_inst'])

# Mostrar código institucional (oculto al usuario pero disponible para uso interno)
st.session_state['selected_institution_code'] = cod_inst

# Función para formatear números con separador de miles y manejar valores nulos
def format_number(value):
    if pd.isna(value) or value == "" or value is None:
        return "-"
    try:
        # Convertir a entero y formatear con separador de miles
        return f"{int(value):,}".replace(",", ".")
    except (ValueError, TypeError):
        return "-"

# Mapeo de categorías y desagregaciones
categoria_map = {
    0: "TOTAL",
    1: "Nivel de carrera",
    2: "Jornada", 
    3: "Modalidad"
}

desagregacion_map = {
    0: {0: "TOTAL"},
    1: {
        1: "Bachillerato o similar",
        2: "TNS",
        3: "Título Profesional", 
        4: "Licenciatura",
        5: "Título y Licenciatura",
        6: "Especialidad Médica",
        7: "Diplomado",
        8: "Postítulo",
        9: "Magister",
        10: "Doctorado"
    },
    2: {
        1: "Diurno",
        2: "Vespertino",
        3: "Semipresencial",
        4: "A distancia",
        5: "Otro"
    },
    3: {
        1: "Presencial",
        2: "Semipresencial", 
        3: "No presencial"
    }
}

# Función para cargar y procesar datos de tablas
def procesar_tabla(nombre_archivo, cod_inst):
    try:
        df_tab = pd.read_csv(nombre_archivo, sep=';', encoding='utf-8')
    except FileNotFoundError:
        st.error(f"No se encontró el archivo '{nombre_archivo}'. Asegúrate de que esté en el mismo directorio.")
        return None
    except Exception as e:
        st.error(f"Error al cargar el archivo {nombre_archivo}: {e}")
        # Intentar con encoding alternativo
        try:
            df_tab = pd.read_csv(nombre_archivo, sep=';', encoding='latin-1')
        except Exception as e2:
            st.error(f"Error también con encoding alternativo: {e2}")
            return None
    
    # Filtrar datos por institución seleccionada
    df_filtered = df_tab[df_tab['cod_inst'] == cod_inst]
    
    # Aplicar mapeos al DataFrame filtrado
    df_filtered['Categoría'] = df_filtered['categoria'].map(categoria_map)
    df_filtered['Desagregación'] = df_filtered.apply(
        lambda row: desagregacion_map.get(row['categoria'], {}).get(row['desagregacion'], ""), 
        axis=1
    )
    
    # Aplicar formato a las columnas de años
    year_columns = [col for col in df_filtered.columns if col.startswith('programas')]
    for year_col in year_columns:
        df_filtered[year_col] = df_filtered[year_col].apply(format_number)
    
    return df_filtered

# Sección DIMENSIÓN 1
st.divider()
st.header("DIMENSIÓN 1: DOCENCIA Y RESULTADOS DEL PROCESO DE FORMACIÓN")

# Indicador 01: Número de programas vigentes
st.subheader("Criterio 1: Oferta formativa")
st.write("**Indicador 01: Número de programas vigentes.**")

# Cargar y mostrar datos para Indicador 01
df_tab1 = procesar_tabla("tab1.csv", cod_inst)
if df_tab1 is not None:
    # Crear tabla para mostrar
    table_data_01 = []
    for _, row in df_tab1.iterrows():
        table_data_01.append({
            'Categoría': row['Categoría'],
            'Desagregación': row['Desagregación'],
            '2021': row['programas2021'],
            '2022': row['programas2022'], 
            '2023': row['programas2023'],
            '2024': row['programas2024'],
            '2025': row['programas2025']
        })

    # Mostrar tabla
    if table_data_01:
        df_display_01 = pd.DataFrame(table_data_01)
        st.dataframe(df_display_01, use_container_width=True, hide_index=True)
    else:
        st.warning("No se encontraron datos para la institución seleccionada en el Indicador 01.")

# Indicador 03: Matrícula total
st.subheader("Criterio 3: Acceso y progresión de los estudiantes")
st.write("**Indicador 03: Matrícula total.**")

# Cargar y mostrar datos para Indicador 03
df_tab3 = procesar_tabla("tab3.csv", cod_inst)
if df_tab3 is not None:
    # Crear tabla para mostrar
    table_data_03 = []
    for _, row in df_tab3.iterrows():
        table_data_03.append({
            'Categoría': row['Categoría'],
            'Desagregación': row['Desagregación'],
            '2021': row['programas2021'],
            '2022': row['programas2022'], 
            '2023': row['programas2023'],
            '2024': row['programas2024'],
            '2025': row['programas2025']
        })

    # Mostrar tabla
    if table_data_03:
        df_display_03 = pd.DataFrame(table_data_03)
        st.dataframe(df_display_03, use_container_width=True, hide_index=True)
    else:
        st.warning("No se encontraron datos para la institución seleccionada en el Indicador 03.")

# Fuente
st.caption("Fuente: Elaboración propia en base a datos SIES (Mineduc)")

# Indicador 04: Matrícula primer año
st.write("**Indicador 04: Matrícula primer año.**")

# Cargar y mostrar datos para Indicador 03
df_tab4 = procesar_tabla("tab4.csv", cod_inst)
if df_tab4 is not None:
    # Crear tabla para mostrar
    table_data_04 = []
    for _, row in df_tab4.iterrows():
        table_data_04.append({
            'Categoría': row['Categoría'],
            'Desagregación': row['Desagregación'],
            '2021': row['programas2021'],
            '2022': row['programas2022'], 
            '2023': row['programas2023'],
            '2024': row['programas2024'],
            '2025': row['programas2025']
        })

    # Mostrar tabla
    if table_data_04:
        df_display_04 = pd.DataFrame(table_data_04)
        st.dataframe(df_display_04, use_container_width=True, hide_index=True)
    else:
        st.warning("No se encontraron datos para la institución seleccionada en el Indicador 04.")

# Fuente
st.caption("Fuente: Elaboración propia en base a datos SIES (Mineduc)")
