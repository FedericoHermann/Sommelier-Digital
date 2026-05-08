import numpy as np
import streamlit as st

from src.explainability import explain_recommendation
from src.load_data import load_wine_data
from src.preprocess import build_feature_matrix, add_wine_type
from src.recommender import recommend_wines


# =========================================
# MARIDAJE POR VINO (SE MANTIENE)
# =========================================
def suggest_pairing(row):
    pairings = []

    acidity = row["acidity"]
    sweetness = row["sweetness"]
    tannin = row["tannin"]
    body = row["body"]
    wine_type = row.get("type", "")

    if wine_type == "Tinto":
        pairings += [
            "Carnes rojas (asado, bife, cordero)",
            "Parrilla y carnes ahumadas",
            "Hamburguesas gourmet",
            "Pastas con salsa de tomate",
            "Quesos duros (parmesano, gruyere)",
            "Quesos azules",
            "Hongos salteados",
            "Embutidos (salame, chorizo)"
        ]

    elif wine_type == "Blanco":
        pairings += [
            "Pescados y mariscos",
            "Pollo a la plancha",
            "Ensaladas frescas",
            "Quesos frescos (cabra, ricotta)",
            "Vegetales grillados",
            "Sushi",
            "Pastas con salsa blanca",
            "Risotto"
        ]

    elif wine_type == "Rosé":
        pairings += [
            "Ensaladas completas",
            "Mariscos",
            "Pescado grillado",
            "Pollo",
            "Charcutería",
            "Quesos suaves",
            "Pizza",
            "Comida mediterránea"
        ]

    elif wine_type == "Naranjo":
        pairings += [
            "Pollo especiado",
            "Cerdo",
            "Cocina asiática",
            "Curry",
            "Vegetales intensos (berenjena)",
            "Hongos",
            "Quesos curados",
            "Platos ahumados"
        ]

    elif wine_type == "Espumante":
        pairings += [
            "Frituras (tempura, pollo frito)",
            "Papas fritas",
            "Mariscos",
            "Sushi",
            "Quesos blandos",
            "Jamón / charcutería",
            "Snacks salados",
            "Aperitivos"
        ]

    elif wine_type == "Dulce":
        pairings += [
            "Postres",
            "Tortas",
            "Chocolate",
            "Frutas",
            "Queso azul",
            "Foie gras",
            "Cocina picante",
            "Frutos secos"
        ]

    elif wine_type == "Fortificado":
        pairings += [
            "Quesos intensos",
            "Chocolate amargo",
            "Frutos secos",
            "Postres",
            "Foie gras",
            "Tarta de frutas",
            "Pâté",
            "Café / sobremesa"
        ]

    return list(set(pairings))


# =========================================
# UI COMPLETA (SIN TOCAR UX)
# =========================================
def render_pairing_ui():

    # GRASA
    st.subheader("Estructura principal del plato")

    FAT_SCALES = {
        1: ("Muy liviano", "Platos frescos, sin grasa perceptible (ensaladas, ceviches, vegetales al vapor o hervidos)."),
        2: ("Liviano", "Preparaciones suaves, con poca grasa (pescado al vapor, pollo a la plancha, carnes magras, vegetales asados)."),
        3: ("Equilibrado", "Balance entre frescura y untuosidad (pastas, aves, platos mixtos, hortalizas asadas de superficies crocantes con especias)."),
        4: ("Untuoso", "Textura rica, con presencia de grasa (cremas, quesos, frituras suaves)."),
        5: ("Pesado", "Alta carga grasa, intensa y persistente (frituras, carnes grasas, salsas densas)."),
    }

    fat_level = st.slider("Pesadez / Complejidad del plato", 1, 5, 3)
    word, description = FAT_SCALES[fat_level]
    st.markdown(f"*{word} ({fat_level}) — {description}*")

    # SALSAS
    SAUCE_SCALES = {
        1: ("Muy simple", "Sin acompañamientos o muy ligeros (a la plancha, hervidos, sin salsa)."),
        2: ("Sutil", "Acompañamientos suaves que no dominan (guarniciones simples, aceite de oliva, hierbas)."),
        3: ("Equilibrado", "El plato tiene acompañamientos y salsas que acompañan sin sobresalir (pures simples, cremas livianas, vegetales asados)."),
        4: ("Expresivo", "Salsas o guarniciones con sabor marcado (tomate, especias, reducciones)."),
        5: ("Dominante", "La salsa o acompañamiento define el plato (cremas intensas, salsas complejas)."),
    }

    st.markdown("---")
    st.subheader("Acompañamientos y salsas del plato")

    sauce_level = st.slider("Salsas", 1, 5, 3)
    word, description = SAUCE_SCALES[sauce_level]
    st.markdown(f"*{word} ({sauce_level}) — {description}*")

    # ACIDEZ
    ACIDITY_SCALES = {
        1: ("Muy baja", "Sin acidez perceptible."),
        2: ("Suave", "Acidez leve que aporta frescura."),
        3: ("Equilibrada", "Acidez integrada."),
        4: ("Marcada", "Acidez evidente."),
        5: ("Intensa", "Acidez protagonista."),
    }

    st.markdown("---")
    st.subheader("Percepción de paladar del plato")

    acid_level = st.slider("Acidez", 1, 5, 3)
    word, description = ACIDITY_SCALES[acid_level]
    st.markdown(f"*{word} ({acid_level}) — {description}*")

    return fat_level, acid_level, sauce_level


# =========================================
# VECTOR
# =========================================
def build_food_vector(fat_level, acid_level, sauce_level):

    acidity = 3
    sweetness = 2
    tannin = 2
    body = 3
    persistence = 3
    complexity = 3

    if fat_level >= 4:
        body += 1
        tannin += 1
    elif fat_level <= 2:
        body -= 1

    if acid_level >= 4:
        acidity += 1
    elif acid_level <= 2:
        acidity -= 1

    if sauce_level >= 4:
        complexity += 1
        persistence += 1
    elif sauce_level <= 2:
        complexity -= 1

    return np.array([
        acidity / 5,
        sweetness / 5,
        tannin / 5,
        body / 5,
        persistence / 5,
        complexity / 5
    ])


# =========================================
# PANTALLA COMPLETA (MODO 2)
# =========================================
def render_pairing_screen():

    st.title("🍽️ Maridaje inverso")

    st.markdown("---")
    if st.button("← Volver"):
        st.session_state.mode = None
        st.rerun()
    st.markdown("---")

    fat_level, acid_level, sauce_level = render_pairing_ui()

    if st.button("Recomendar vino 🍷"):

        df = load_wine_data()
        df = add_wine_type(df)

        features = build_feature_matrix(df)[:, :6]

        user_vector = build_food_vector(
            fat_level, acid_level, sauce_level
        )

        reco = recommend_wines(df, features, user_vector)

        st.success("Estos vinos acompañan muy bien tu plato:")

        for _, row in reco.head(3).iterrows():

            # título
            st.markdown(f"**{row['varietal']} ({row['type']}) — {row['country']}**")

            # datos técnicos
            st.markdown(
                f"- Alcohol: {row['alcohol_pct']}%  \n"
                f"- Puntaje: {row['rating']} pts  \n"
                f"- Segmento: {row['price_segment']}  \n"
                f"- Guarda potencial: {row['aging_potential_years']} años"
            )

            # EXPLAINABILITY REUTILIZADO
            st.caption(
                explain_recommendation(row, user_vector, context="pairing")
            )

            st.markdown("---")