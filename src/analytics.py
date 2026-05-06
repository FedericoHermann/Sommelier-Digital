import matplotlib.pyplot as plt
import numpy as np


def plot_radar_chart(row, user_vector=None):

    # ======================================
    # 1. CONFIGURACIÓN GLOBAL (CRISP TEXT)
    # ======================================
    # Fuente estable y bien renderizada en Cloud
    plt.rcParams["font.family"] = "DejaVu Sans"

    # Anti-aliasing activado (mejora bordes)
    plt.rcParams["text.antialiased"] = True
    plt.rcParams["lines.antialiased"] = True

    # ======================================
    # 2. VARIABLES DEL GRÁFICO
    # ======================================
    labels = ["Acidez", "Dulzor", "Taninos", "Cuerpo", "Complejidad", "Persistencia"]

    wine_values = [
        row["acidity"],
        row["sweetness"],
        row["tannin"],
        row["body"],
        row["complexity"],
        row["persistence"]
    ]

    # Cerrar el loop del radar
    wine_values += [wine_values[0]]

    # Ángulos del radar
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += [angles[0]]

    # ======================================
    # 3. LIENZO (ALTA DEFINICIÓN)
    # ======================================
    # DPI alto = clave para evitar blur en Streamlit Cloud
    fig, ax = plt.subplots(figsize=(3, 3), dpi=600, subplot_kw=dict(polar=True))

    # Ajuste de márgenes → controla tamaño visual del radar
    fig.subplots_adjust(left=0.32, right=0.68, top=0.68, bottom=0.32)

    # ======================================
    # 4. COLORES
    # ======================================
    accent_color = "#CB2508"   # tono principal (vino)
    text_color = "#B8B8B8"     # gris suave (sin halo)

    # Fondo consistente con la app
    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    # ======================================
    # 5. RADAR (VINO)
    # ======================================
    ax.plot(
        angles,
        wine_values,
        linewidth=0.5,              # fino → elegante
        color=accent_color
    )

    ax.fill(
        angles,
        wine_values,
        color=accent_color,
        alpha=0.20                 # liviano → no invasivo
    )

    # ======================================
    # 6. LABELS (TIPOGRAFÍA EDITORIAL)
    # ======================================
    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(
        labels,
        color=text_color,
        fontsize=6               # pequeño pero definido
    )

    # centrado visual de etiquetas
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("center")
        label.set_path_effects([])  

    # ======================================
    # 7. ESCALA RADIAL
    # ======================================
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels([])        

    # ======================================
    # 8. GRID (SUAVE Y ELEGANTE)
    # ======================================
    ax.grid(
        color="#444444",
        linestyle="dotted",
        linewidth=0.5,            # muy fino
        alpha=0.5                  # suave
    )

    # borde del radar (muy sutil)
    ax.spines["polar"].set_color("#2A2A2A")
    ax.spines["polar"].set_linewidth(0.5)

    # ======================================
    # 9. ESPACIADO FINAL
    # ======================================
    # acerca labels al radar
    ax.tick_params(pad=0.8)

    return fig
