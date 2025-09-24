import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dashboard público", layout="wide")

st.title("📊 Dashboard público con Streamlit")
st.markdown("Ejemplo simple desplegado desde GitHub")

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
