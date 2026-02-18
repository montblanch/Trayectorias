import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Calculadora Balística",
    page_icon="🚀",
    layout="centered"
)

# --- 2. CABECERA ---
st.title("🚀 Analizador de Trayectorias")
st.write("Introduce los valores a, b y c en el menú y pulsa el botón.")

# --- 3. BARRA LATERAL (Solo para datos) ---
with st.sidebar:
    st.header("⚙️ Datos de la Ecuación")
    # Inputs numéricos
    a = st.number_input("Valor de a:", value=0.0, step=0.1, format="%.2f")
    b = st.number_input("Valor de b:", value=0.0, step=0.1, format="%.2f")
    c = st.number_input("Valor de c:", value=0.0, step=0.1, format="%.2f")

# --- 4. BOTÓN (AHORA EN LA PANTALLA PRINCIPAL) ---
# Lo hemos sacado de la barra lateral para que siempre se vea
calcular = st.button("Calcular Resultado", type="primary", use_container_width=True)

# --- 5. LÓGICA Y RESULTADOS ---
if calcular:
    st.divider()

    # Cálculos
    delta = b**2 - 4*a*c
    
    # Variables
    tipo = ""
    riesgo = ""
    color_riesgo = ""
    mensaje_corte = ""

    # Lógica de clasificación
    if a == 0:
        tipo = "Rectilínea (No balística)"
        riesgo = "Nulo"
        color_riesgo = "blue"
        mensaje_corte = "No aplica"
    else:
        if a > 0:
            tipo = "Parábola hacia ARRIBA (Valle)"
        else:
            tipo = "Parábola hacia ABAJO (Proyectil)"
            
        if delta < 0:
            mensaje_corte = "No toca el suelo"
        elif delta == 0:
            mensaje_corte = "Roza el suelo (1 punto)"
        else:
            mensaje_corte = "Impacta en el suelo (2 puntos)"

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

    # Mostrar Alertas
    if color_riesgo == "red":
        st.error(f"🚨 RIESGO: {riesgo}")
    elif color_riesgo == "orange":
        st.warning(f"⚠️ RIESGO: {riesgo}")
    elif color_riesgo == "green":
        st.success(f"✅ RIESGO: {riesgo}")
    else:
        st.info(f"ℹ️ RIESGO: {riesgo}")

    # Métricas
    col1, col2 = st.columns(2)
    col1.metric("Trayectoria", tipo.split("(")[0])
    col2.metric("Discriminante", f"{delta:.2f}")

    # --- 6. GRÁFICA ---
    st.subheader("Gráfica")
    
    # Eje X inteligente
    if a != 0:
        vertice_x = -b / (2*a)
        span = max(abs(vertice_x)*1.5, 10)
        if delta > 0:
             x1 = (-b + np.sqrt(delta)) / (2*a)
             x2 = (-b - np.sqrt(delta)) / (2*a)
             span = max(abs(x1), abs(x2)) * 1.2
        x = np.linspace(vertice_x - span, vertice_x + span, 400)
    else:
        x = np.linspace(-10, 10, 200)

    y = a*x**2 + b*x + c

    fig, ax = plt.subplots()
    ax.plot(x, y, label='Trayectoria', color='blue', linewidth=2)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='gray', linestyle=':')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    
    st.pyplot(fig, use_container_width=True)
