import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA (Debe ser lo primero) ---
# Ajustamos el título de la pestaña y el icono.
# layout="centered" es el predeterminado y suele verse mejor en móviles que "wide".
st.set_page_config(
    page_title="Trayectorias Balísticas",
    page_icon="💥",
    layout="centered"
)

# --- CABECERA CON IMAGEN REAL ---
# URL de una imagen de dominio público de un Tomahawk (Wikimedia Commons)
tomahawk_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Tomahawk_Block_IV_cruise_missile_conducts_a_flight_test.jpg/800px-Tomahawk_Block_IV_cruise_missile_conducts_a_flight_test.jpg"

# Mostramos la imagen. 'use_container_width=True' es CLAVE para móviles.
st.image(tomahawk_url, caption="Misil de crucero BGM-109 Tomahawk", use_container_width=True)

# Título principal (sin el emoji del cohete)
st.title("Analizador de Trayectorias Balísticas")
st.write("Introduce los coeficientes de la ecuación parabólica: $y = ax^2 + bx + c$")

# --- 1. ENTRADAS (Barra lateral móvil) ---
# En móviles, la barra lateral se convierte en un menú hamburguesa (≡) arriba a la izquierda.
with st.sidebar:
    st.header("⚙️ Parámetros de Lanzamiento")
    st.write("Ajusta los valores:")
    # Usamos st.number_input para mayor precisión
    a = st.number_input("Curvatura (a):", value=0.0, step=0.1, format="%.2f", help="Si es negativo, la curva cae hacia abajo.")
    b = st.number_input("Inclinación inicial (b):", value=0.0, step=0.1, format="%.2f")
    c = st.number_input("Altura inicial (c):", value=0.0, step=0.1, format="%.2f", help="Punto de partida en el eje Y.")
    
    st.divider()
    # Botón principal
    calcular = st.button("🚀 Iniciar Análisis", type="primary", use_container_width=True)

# --- 2. LÓGICA Y RESULTADOS ---
if calcular:
    st.divider()

    # -- Lógica Matemática --
    delta = b**2 - 4*a*c
    
    tipo = ""
    riesgo = ""
    color_riesgo = ""
    mensaje_corte = ""

    if a == 0:
        tipo = "Trayectoria Rectilínea (No balística)"
        riesgo = "Nulo"
        color_riesgo = "blue"
        mensaje_corte = "No aplica el discriminante"
    else:
        # Tipo
        if a > 0:
            tipo = "Parábola abierta hacia ARRIBA (Valle)"
        else:
            tipo = "Parábola abierta hacia ABAJO (Proyectil)"
            
        # Corte eje X
        if delta < 0:
            mensaje_corte = "No toca el suelo (Eje X)"
        elif delta == 0:
            mensaje_corte = "Toca el suelo en 1 punto (Rozamiento)"
        else:
            mensaje_corte = "Impacta en el suelo en 2 puntos"

        # Riesgo
        if a > 0 and delta < 0:
            riesgo = "Bajo"
            color_riesgo = "green"
        elif delta == 0:
            riesgo = "Medio"
            color_riesgo = "orange"
        elif a < 0 and delta > 0:
            riesgo = "Alto (Impacto confirmado)"
            color_riesgo = "red"
        else:
            riesgo = "No clasificado"
            color_riesgo = "gray"

    # -- Mostrar Alertas --
    if color_riesgo == "red":
        st.error(f"🚨 **NIVEL DE RIESGO: {riesgo.upper()}**")
    elif color_riesgo == "orange":
        st.warning(f"⚠️ **Nivel de Riesgo: {riesgo}**")
    elif color_riesgo == "green":
        st.success(f"✅ **Nivel de Riesgo: {riesgo}**")
    else:
        st.info(f"ℹ️ Nivel de Riesgo: {riesgo}")

    # -- Mostrar Métricas (En móviles se apilarán automáticamente) --
    col1, col2 = st.columns(2)
    col1.metric("Tipo de Curva", tipo.split("(")[0]) # Simplificamos texto
    col2.metric("Impactos en Suelo", f"{delta:.2f}", help="Valor del discriminante (Δ)")
    st.caption(f"Detalle: {mensaje_corte}")


    # --- 3. GRÁFICA RESPONSIVE ---
    st.subheader("Visualización de la Trayectoria")
    
    # Rango dinámico para que la gráfica se vea bien
    if a != 0:
        vertice_x = -b / (2*a)
        # Calculamos un rango alrededor del vértice
        span = max(abs(vertice_x)*1.5, 10) 
        if delta > 0:
             # Si hay cortes, intentamos incluir los puntos de corte
             x1 = (-b + np.sqrt(delta)) / (2*a)
             x2 = (-b - np.sqrt(delta)) / (2*a)
             span = max(abs(x1), abs(x2)) * 1.2
        x = np.linspace(vertice_x - span, vertice_x + span, 400)
    else:
        x = np.linspace(-10, 10, 200)

    y = a*x**2 + b*x + c

    fig, ax = plt.subplots(figsize=(8, 4)) # Hacemos la figura más ancha que alta
    ax.plot(x, y, label='Trayectoria', color='#d62728', linewidth=2.5) # Color rojo misil
    ax.axhline(0, color='black', linewidth=1.5, linestyle='--') # Suelo
    ax.axvline(0, color='gray', linewidth=1, linestyle=':') # Eje Y
    
    # Rellenar bajo la curva si es riesgo alto para efecto dramático
    if riesgo.startswith("Alto"):
         ax.fill_between(x, y, 0, where=(y>0), color='#d62728', alpha=0.2)

    ax.set_title(f"y = {a:.2f}x² + {b:.2f}x + {c:.2f}")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_xlabel("Distancia")
    ax.set_ylabel("Altura")
    ax.legend()
    
    # --- CLAVE PARA MÓVIL: use_container_width=True ---
    st.pyplot(fig, use_container_width=True)

else:
    st.info("👈 Abre la barra lateral (menú ≡) para introducir los parámetros de lanzamiento.")
