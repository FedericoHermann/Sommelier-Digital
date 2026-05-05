import matplotlib.pyplot as plt
import numpy as np



def plot_radar_chart(row, user_vector=None):

    labels = ["Acidez", "Dulzor", "Taninos", "Cuerpo", "Complejidad", "Persistencia"]

    wine_values = [
        row["acidity"],
        row["sweetness"],
        row["tannin"],
        row["body"],
        row["complexity"],
        row["persistence"]
    ]

    # cerrar círculo
    wine_values += [wine_values[0]]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += [angles[0]]

    # para cambiar tamaño
    fig, ax = plt.subplots(figsize=(1, 1), subplot_kw=dict(polar=True))

    # para cambiar estilos de color 
    accent_color = "#E0430F"   
    user_color = "#F8151566"     

    # fondo negro
    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    # vino
    ax.plot(angles, wine_values, linewidth=0.3, color=accent_color)
    ax.fill(angles, wine_values, color=accent_color, alpha=0.25)

    # usuario (línea punteada)
    if user_vector is not None:
        user_values = user_vector[:6].tolist()
        user_values += [user_values[0]]
        ax.plot(angles, user_values, linestyle="dashed", linewidth=0.3, color=user_color)

    # etiquetas
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color="white", fontsize=2)

    # escala radial
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels([], color="white", fontsize=2)

    # grilla en gris suave
    ax.grid(color="gray", linestyle="dotted", linewidth=0.3)

    return fig
