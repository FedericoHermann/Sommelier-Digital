import numpy as np

# Variables estructurales (escala 1–5)
STRUCTURAL_COLS = [
    "acidity",
    "sweetness",
    "tannin",
    "body",
    "persistence",
    "complexity"
]

# Variables aromáticas (binarias)
AROMA_COLS = [
    "aroma_red_fruit",
    "aroma_black_fruit",
    "aroma_white_yellow_fruit",  
    "aroma_floral",
    "aroma_spice",
    "aroma_wood",
    "aroma_mineral",
    "aroma_herbal"
]

def build_feature_matrix(df):
    """
    Construye la matriz de features normalizadas
    usada para el cálculo de similitud.
    """
    # Normalizar estructura a 0–1
    structural = df[STRUCTURAL_COLS] / 5.0

    # Aromas ya son binarios
    aromas = df[AROMA_COLS]

    features = np.hstack([structural.values, aromas.values])
    return features