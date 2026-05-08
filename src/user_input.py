import numpy as np

STRUCTURAL_FEATURES = [
    "acidity",
    "sweetness",
    "tannin",
    "body",
    "persistence",
    "complexity"
]

# IMPORTANTE: el orden debe coincidir con preprocess.py
AROMA_MAPPING = {
    "fruta roja": "aroma_red_fruit",
    "fruta negra": "aroma_black_fruit",
    "fruta blanca / amarilla": "aroma_white_yellow_fruit",  # <-- NUEVA
    "floral": "aroma_floral",
    "especias": "aroma_spice",
    "madera": "aroma_wood",
    "mineral": "aroma_mineral",
    "herbal": "aroma_herbal",
}


def build_user_vector(
    acidity: int,
    sweetness: int,
    tannin: int,
    body: int,
    persistence: int,
    complexity: int,
    aromas_selected: list[str] | None = None
) -> np.ndarray:
    """
    Construye el vector sensorial del usuario validado y normalizado.
    """

    # --- Validación estructural ---
    structural_values = [
        acidity, sweetness, tannin, body, persistence, complexity
    ]

    for name, value in zip(STRUCTURAL_FEATURES, structural_values):
        if not isinstance(value, int):
            raise TypeError(f"{name} debe ser un entero entre 1 y 5")
        if value < 1 or value > 5:
            raise ValueError(f"{name} fuera de rango (1–5)")

    # Normalización 1–5 → 0–1
    normalized_structural = [v / 5.0 for v in structural_values]

    # --- Aromas ---
    aroma_vector = [0] * len(AROMA_MAPPING)

    if aromas_selected:
        for aroma in aromas_selected:
            if aroma not in AROMA_MAPPING:
                raise ValueError(f"Aroma no reconocido: {aroma}")
            idx = list(AROMA_MAPPING.keys()).index(aroma)
            aroma_vector[idx] = 1

    # Vector final
    user_vector = np.array(normalized_structural + aroma_vector)
    return user_vector
