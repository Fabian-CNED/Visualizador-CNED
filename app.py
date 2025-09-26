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

# Define listado de instituciones
instituciones_df = pd.DataFrame({
    'id': range(1, 201),
    'nombre': [f"Institución {i}" for i in range(1, 201)]
})

# Crear el selectbox
institucion_seleccionada = st.selectbox(
    "Selecciona una institución:",
    options=instituciones_df['nombre'].tolist(),
    index=0,
    help="Elige una institución de educación superior para ver sus datos"
)

# Obtener el ID de la institución seleccionada
institucion_id = instituciones_df[instituciones_df['nombre'] == institucion_seleccionada]['id'].iloc[0]

st.write(f"ID de la institución seleccionada: {institucion_id}")
Con datos cargados desde archivo:



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
