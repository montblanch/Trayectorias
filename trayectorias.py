import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. CONFIGURACIÓN DE PÁGINA (Debe ser lo primero) ---
st.set_page_config(
    page_title="Trayectorias Balísticas",
    page_icon="💥",
    layout="centered"
)

# --- 2. CABECERA E IMAGEN DEL MISIL ---
# Usamos el enlace directo al archivo original para evitar errores de carga
tomahawk_url = "https://upload.wikimedia.org/wikipedia/commons/c/c6/Tomahawk_Block_IV_cruise_missile_conducts_a_flight_test.jpg"

try:
    st.image(tomahawk_url, caption="Misil de crucero BGM-109 Tomahawk", use_container_width=True)
except Exception:
    # Si la imagen falla, mostramos un aviso pero la app sigue funcionando
    st.warning("⚠️ No se pudo cargar la imagen del servidor, pero el cálculo funciona.")

st.title("Analizador de Trayectorias Balísticas")
st.write("Introduce los coeficientes de la ecuación parabólica: $y = ax^2 + bx + c$")

# --- 3. BARRA LATERAL (INPUTS) ---
with st.sidebar:
    st.header("⚙️ Parámetros de Lanzamiento")
    st.write("Ajusta los valores:")
    
    # Inputs numéricos
    a = st.number_input("Curvatura (a):", value=0.0, step=0.1, format="%.2f", help="Negativo = hacia abajo (proyectil).")
    b = st.number_input("Inclinación inicial (b):", value=0.0, step=0.1, format="%.2f")
    c = st.number_input("Altura inicial (c):", value=0.0, step=0.1, format="%.2f")
    
    st.divider()
    # Botón de cálculo
    calcular = st.button("🚀 Iniciar Análisis", type="primary", use_container_width=True)

# --- 4. LÓGICA DEL PROGRAMA ---
if calcular:
    st.divider()
