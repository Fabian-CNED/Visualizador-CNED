import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Visualizador CNED", layout="wide")

st.markdown(
    """
    <div style="text-align: right;">
        <img src="https://cned.cl/wp-content/uploads/2023/10/cned_s_fondo.png" width="100">
    </div>
    """,
    unsafe_allow_html=True
)

st.title("**VISUALIZADOR DE DATOS INSTITUCIONALES**")
st.subheader("Última actualización: 30 de septiembre de 2025")
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
