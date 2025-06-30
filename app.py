import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🧮 Calculadora de Interés Compuesto")

# Sidebar
with st.sidebar:
    st.header("⚙️ Parámetros")
    initial = st.number_input("Capital inicial (€)", min_value=0.0, value=1000.0)
    rate = st.number_input("Tasa de interés anual (%)", min_value=0.0, value=5.0)
    years = st.number_input("Años de inversión", min_value=1, value=10)
    monthly = st.number_input("Aporte mensual (€)", min_value=0.0, value=100.0)

# Cálculos
if st.button("Calcular"):
    periods = years * 12
    monthly_rate = rate / 100 / 12
    future_value = np.fv(monthly_rate, periods, -monthly, -initial)
    
    # Gráfico
    fig, ax = plt.subplots()
    x = np.arange(years + 1)
    y = [initial * (1 + rate/100)**t + monthly*12 * (((1 + rate/100)**t - 1)/(rate/100)) for t in x]
    ax.plot(x, y, color='#4ECDC4', linewidth=3)
    ax.set_title("Evolución del Capital")
    ax.set_xlabel("Años")
    ax.set_ylabel("Balance (€)")
    ax.grid(True)
    
    # Resultados
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Valor Final", f"€{future_value:,.2f}")
    with col2:
        st.metric("Ganancias", f"€{future_value - initial - (monthly*periods):,.2f}")
    
    st.pyplot(fig)