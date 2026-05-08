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


# =========================================================
# 🆕 CLASIFICACIÓN DE TIPO DE VINO
# =========================================================
def get_wine_type(varietal):
    v = varietal.lower()

    # Rosé
    if "rose" in v:
        return "Rosé"

    # Orange
    if "orange" in v:
        return "Naranjo"

    # Espumantes
    if v in ["champagne", "cava", "prosecco"]:
        return "Espumante"

    # Fortificados
    if v in ["oporto", "jerez"]:
        return "Fortificado"

    # Dulces
    if "late harvest" in v:
        return "Dulce"

    # Tintos
    tintos = [
        "malbec", "cabernet sauvignon", "merlot", "syrah",
        "pinot noir", "tempranillo", "garnacha",
        "zinfandel", "nebbiolo", "bonarda", "carmenere", "sangiovese"
    ]

    # Blancos
    blancos = [
        "chardonnay", "sauvignon blanc", "riesling",
        "chenin blanc", "semillon", "torrontes"
    ]

    if v in tintos:
        return "Tinto"
    if v in blancos:
        return "Blanco"

    return "Otro"


def add_wine_type(df):
    """
    Agrega la columna 'type' al dataframe sin alterar
    las features utilizadas por el modelo.
    """
    df["type"] = df["varietal"].apply(get_wine_type)
    return df


# =========================================================
# 🧠 FEATURE MATRIX (NO TOCAR LÓGICA)
# =========================================================
def build_feature_matrix(df):
    """
    Construye la matriz de features normalizadas
    usada para el cálculo de similitud.
    """
    # Normalizar estructura a 0–1
    structural = df[STRUCTURAL_COLS] / 5.0

    aromas = df[AROMA_COLS]

    features = np.hstack([structural.values, aromas.values])
    return features
