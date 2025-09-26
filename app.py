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

# Supongamos que tienes un DataFrame con las instituciones
instituciones_df = pd.DataFrame({
    'id': range(1, 201),
    'nombre': [f"Institución {i}" for i in range(1, 201)]
})

# Sidebar para mejor organización
with st.sidebar:
    st.header("🏫 Selección de Institución")
    
    institucion_seleccionada = st.selectbox(
        "Institución:",
        instituciones_df['nombre'].tolist(),
        key="selector_institucion"
    )
    
    # También puedes agregar un buscador
    buscar = st.text_input("Buscar institución:", "")

# Filtrar opciones si se usa el buscador
if buscar:
    opciones_filtradas = [inst for inst in instituciones_df['nombre'] if buscar.lower() in inst.lower()]
    if opciones_filtradas:
        institucion_seleccionada = st.selectbox(
            "Resultados de búsqueda:",
            opciones_filtradas
        )
# Datos de ejemplo
df = pd.DataFrame({
    "x": np.arange(0, 20),
    "serie A": np.random.randn(20).cumsum(),
    "serie B": np.random.randn(20).cumsum()
})

# Gráfico
st.line_chart(df.set_index("x"))

# Tabla
st.subheader("Datos")
st.dataframe(df)
