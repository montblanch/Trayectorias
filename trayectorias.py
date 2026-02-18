import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. CONFIGURACIÓN DE PÁGINA (Debe ser lo primero) ---
# Configura el título de la pestaña del navegador y el icono
st.set_page_config(
    page_title="Calculadora Balística",
    page_icon="🚀",
    layout="centered"
)

# --- 2. CABECERA (Volvemos al cohete emoji que no falla) ---
st.title("🚀 Analizador de Trayectorias Balísticas")
st.write("Introduce los coeficientes de la ecuación parabólica: $y = ax^2 + bx + c$")
st.info("💡 Para móviles: Pulsa la flecha (>) arriba a la izquierda para ver los controles.")

# --- 3. BARRA LATERAL (INPUTS) ---
with st.sidebar:
    st.header("⚙️ Parámetros")
    st.write("Ajusta los valores de la ecuación:")
    
    # Inputs numéricos adaptados para móvil
    a = st.number_input("Curvatura (a):", value=0.0, step=0.1, format="%.2f", help="Si es negativo, la curva cae hacia abajo (proyectil).")
    b = st.number_input("Inclinación inicial (b):", value=0.0, step=0.1, format="%.2f")
    c = st.number_input("Altura inicial (c):", value=0.0, step=0.1, format="%.2f")
