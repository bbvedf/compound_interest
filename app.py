import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.express as px
from io import BytesIO


# Configuración de página
st.set_page_config(layout="wide", page_title="🚀 Calculadora de Interés Compuesto")
st.title("🚀 Calculadora de Interés Compuesto")

# Pestañas principales
tab1, tab2 = st.tabs(["📊 Simulador", "📚 Teoría"])

with tab1:
    # Contenedor de parámetros (arriba, sin sidebar)
    params = st.container(border=True)
    col1, col2, col3 = params.columns(3)
    
    with col1:
        initial = st.number_input("Capital inicial (€)", min_value=0.0, value=10000.0, step=1000.0)
        rate = st.number_input("Tasa anual (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
    
    with col2:
        years = st.number_input("Años", min_value=1, max_value=100, value=10)
        freq_options = {"Anual": 1, "Trimestral": 4, "Mensual": 12}
        freq = st.selectbox("Frecuencia", options=list(freq_options.keys()))
    
    with col3:
        monthly = st.number_input("Aporte periódico (€)", min_value=0.0, value=500.0)
        inflation = st.number_input("Inflación estimada (%)", min_value=0.0, value=2.0, step=0.1)

    # Cálculos
    if st.button("🔄 Calcular", type="primary"):
        periods = years * freq_options[freq]
        periodic_rate = rate / 100 / freq_options[freq]
        future_value = npf.fv(periodic_rate, periods, -monthly, -initial)
        
        # Generar tabla de evolución
        evolution = []
        balance = initial
        for period in range(1, periods + 1):
            interest = balance * periodic_rate
            balance += interest + monthly
            evolution.append({
                "Periodo": period,
                "Año": period // freq_options[freq],
                "Balance": balance,
                "Intereses": interest,
                "Aportes": monthly
            })
        
        df = pd.DataFrame(evolution)
        
        # Gráfico interactivo
        annual_df = df.groupby("Año").agg({"Intereses": "sum", "Aportes": "sum"}).reset_index()

        fig = px.bar(annual_df, x="Año", y=["Intereses", "Aportes"],
                    title="Rendimiento anual",
                    barmode="stack",
                    color_discrete_sequence=["#00B050", "#2EC4B6"],
                    labels={"value": "€"})

        fig.add_scatter(x=annual_df["Año"], y=annual_df["Intereses"].cumsum(),
                        mode="lines+markers",
                        name="Intereses Acumulados",
                        line=dict(color="#C00000", width=3))
        
        # Mostrar resultados
        
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 Valor Final", f"€{future_value:,.2f}")
        with col2:
            st.metric("📈 Ganancias", 
                     f"€{future_value - initial - (monthly*periods):,.2f}",
                     f"{((future_value/(initial + monthly*periods))-1)*100:.1f}%")
        with col3:
            real_gain = (future_value / ((1 + inflation/100)**years)) - initial - (monthly*periods)
            st.metric("🎯 Valor real (aj. inflación)", f"€{real_gain:,.2f}")

        # Tabla resumen anual
        st.subheader("📅 Resumen anual")
        st.dataframe(df.groupby("Año").last().style.format({
            "Balance": "€{:,.2f}",
            "Intereses": "€{:,.2f}"
        }))

        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("""
    ## 📚 Conceptos clave
    ### ¿Qué es el interés compuesto?
    Es el efecto de ganar intereses sobre tus intereses acumulados.
    
    ### Fórmula matemática
    ```
    Valor Final = P × (1 + r/n)^(n×t) + PMT × [((1 + r/n)^(n×t) - 1)/(r/n)]
    ```
    - P = Capital inicial
    - r = Tasa anual
    - n = Frecuencia de capitalización
    - t = Años
    - PMT = Aporte periódico
    """)

# Footer
st.divider()
st.caption("© 2025 - [bbvedf] - Creado con Streamlit")