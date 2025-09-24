import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Visualizador CNED", layout="wide")

col1, col2 = st.columns([1,4])

with col1:
    st.image("https://cned.cl/wp-content/uploads/2023/10/cned_s_fondo.png", width=100)

with col2:
    st.title("VISUALIZADOR DE DATOS INSTITUCIONALES")
    st.subheader("Subtítulo del visualizador")

st.markdown("Contacto: Fabián Ramírez (framirez@cned.cl)")

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
