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
    
    st.divider()
    
    # --- CAMBIO AQUI: Botón "Calcular" estándar ---
    # Hemos quitado 'type="primary"' para que no sea rojo y cambiado el texto.
    calcular = st.button("Calcular", use_container_width=True)

# --- 4. LÓGICA DEL PROGRAMA ---
if calcular:
    st.divider()

    # Cálculos matemáticos
    delta = b**2 - 4*a*c
    
    # Variables de estado
    tipo = ""
    riesgo = ""
    color_riesgo = ""
    mensaje_corte = ""

    # Clasificación (Lógica original)
    if a == 0:
        tipo = "Trayectoria Rectilínea (No balística)"
        riesgo = "Nulo"
        color_riesgo = "blue"
        mensaje_corte = "No aplica el discriminante"
    else:
        # Concavidad
        if a > 0:
            tipo = "Parábola abierta hacia ARRIBA (Valle)"
        else:
            tipo = "Parábola abierta hacia ABAJO (Proyectil)"
            
        # Discriminante (Cortes con eje X)
        if delta < 0:
            mensaje_corte = "No toca el suelo (Eje X)"
        elif delta == 0:
            mensaje_corte = "Toca el suelo en 1 punto (Rozamiento)"
        else:
            mensaje_corte = "Impacta en el suelo en 2 puntos"

        # Nivel de Riesgo
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

    # --- 5. MOSTRAR RESULTADOS ---
    
    # Alertas de colores según el riesgo
    if color_riesgo == "red":
        st.error(f"🚨 **RESULTADO: RIESGO {riesgo.upper()}**")
    elif color_riesgo == "orange":
        st.warning(f"⚠️ **Resultado: Riesgo {riesgo}**")
    elif color_riesgo == "green":
        st.success(f"✅ **Resultado: Riesgo {riesgo}**")
    else:
        st.info(f"ℹ️ Resultado: Riesgo {riesgo}")

    # Métricas en columnas (se adaptan al móvil)
    col1, col2 = st.columns(2)
    col1.metric("Tipo", tipo.split("(")[0]) 
    col2.metric("Discriminante", f"{delta:.2f}")
    st.caption(f"Detalle del suelo: {mensaje_corte}")

    # --- 6. GRÁFICA RESPONSIVE ---
    st.subheader("Gráfica de la Trayectoria")
    
    # Generación de puntos X para la gráfica con zoom dinámico
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

    # Ecuación Y
    y = a*x**2 + b*x + c

    # Dibujo con Matplotlib
    fig, ax = plt.subplots(figsize=(8, 4)) # Proporción panorámica
    ax.plot(x, y, label='Trayectoria', color='#1f77b4', linewidth=2.5) # Azul estándar
    ax.axhline(0, color='black', linewidth=2, linestyle='-') # Suelo más grueso
    ax.axvline(0, color='gray', linewidth=1, linestyle=':') # Eje Y
    
    # Sombreado rojo si es riesgo alto
    if riesgo.startswith("Alto"):
         ax.fill_between(x, y, 0, where=(y>0), color='red', alpha=0.3)
         ax.set_title(f"¡ALERTA DE IMPACTO! y = {a:.2f}x² + {b:.2f}x + {c:.2f}", color="red")
    else:
         ax.set_title(f"y = {a:.2f}x² + {b:.2f}x + {c:.2f}")

    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_xlabel("Distancia (X)")
    ax.set_ylabel("Altura (Y)")
    ax.legend()
    
    # Mostrar gráfica ajustada al ancho del móvil
    st.pyplot(fig, use_container_width=True)

else:
    # Mensaje de bienvenida
    st.write("👈 Usa el menú de la izquierda para empezar.")
