# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:24:13 2026

@author: jmonar4
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Título y descripción
st.title("🚀 Analizador de Trayectorias")
st.write("Introduce los coeficientes de la ecuación: $y = ax^2 + bx + c$")

# --- 1. ENTRADAS (Barra lateral) ---
with st.sidebar:
    st.header("Parámetros")
    # Usamos st.number_input en lugar de input()
    a = st.number_input("Valor de a", value=0.0, step=0.1)
    b = st.number_input("Valor de b", value=0.0, step=0.1)
    c = st.number_input("Valor de c", value=0.0, step=0.1)
    
    # Botón para calcular
    calcular = st.button("Calcular Trayectoria", type="primary")

# --- 2. LÓGICA (Solo se ejecuta si pulsas el botón) ---
if calcular:
    st.markdown("---") # Una línea separadora visual

    # Variables
    tipo = ""
    riesgo = ""
    color_riesgo = ""

    # Lógica del ejercicio
    delta = b**2 - 4*a*c
    
    if a == 0:
        tipo = "Rectilínea (No balística)"
        riesgo = "Nulo"
        color_riesgo = "blue"
    else:
        if a > 0:
            tipo = "Parábola abierta hacia ARRIBA"
        else:
            tipo = "Parábola abierta hacia ABAJO"
            
        # Riesgo
        if a > 0 and delta < 0:
            riesgo = "Bajo"
            color_riesgo = "green"
        elif delta == 0:
            riesgo = "Medio"
            color_riesgo = "orange"
        elif a < 0 and delta > 0:
            riesgo = "Alto"
            color_riesgo = "red"
        else:
            riesgo = "No clasificado"
            color_riesgo = "gray"

    # --- 3. SALIDAS (Mostrar en pantalla) ---
    
    # Mostramos métricas grandes
    col1, col2 = st.columns(2)
    col1.metric("Tipo de Trayectoria", tipo)
    col2.metric("Nivel de Riesgo", riesgo)
    
    # Mensaje de alerta con color
    if color_riesgo == "red":
        st.error(f"⚠️ Alerta: Riesgo {riesgo}")
    elif color_riesgo == "green":
        st.success(f"✅ Estado: Riesgo {riesgo}")
    else:
        st.info(f"ℹ️ Estado: Riesgo {riesgo}")

    # --- 4. GRÁFICA (El extra visual) ---
    st.subheader("Gráfica de la función")
    
    # Crear datos para la gráfica
    x = np.linspace(-10, 10, 400)
    # Si es parábola, intentamos centrar la vista
    if a != 0:
        vertice_x = -b / (2*a)
        x = np.linspace(vertice_x - 10, vertice_x + 10, 400)
        
    y = a*x**2 + b*x + c

    fig, ax = plt.subplots()
    ax.plot(x, y, label=f'Trayectoria', color='blue', linewidth=2)
    ax.axhline(0, color='black', linewidth=1) # Eje X (Suelo)
    ax.axvline(0, color='black', linewidth=1) # Eje Y
    ax.grid(True, linestyle='--')
    ax.legend()
    
    # Mostrar la gráfica en la web
    st.pyplot(fig)