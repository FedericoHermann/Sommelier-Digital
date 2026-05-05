import numpy as np
from src.explainability import explain_recommendation # Acá va nuestro Someelier digital
from src.load_data import load_wine_data # Carga el dataset de vinos
from src.preprocess import build_feature_matrix # Prepara la matriz de características para similitud
from src.recommender import recommend_wines # Función principal de recomendación
from src.user_input import build_user_vector # Construye el vector de perfil del usuario a partir de sus preferencias


# 1. Cargar datos
df = load_wine_data()
features = build_feature_matrix(df)

# 2. Perfil sensorial del usuario (ejemplo) - más adelante tendra interface de input
user_vector = build_user_vector(
    acidity=4,
    sweetness=2,
    tannin=3,
    body=4,
    persistence=4,
    complexity=4,
    aromas_selected=["fruta negra", "especias"]
)


# 3. Obtener recomendaciones (top 3 por defecto)
recomendadas = recommend_wines(df, features, user_vector)

# 4. Mostrar resultados clave
print(
    recomendadas[
        [
            "varietal",
            "country",
            "alcohol_pct",
            "rating",
            "price_segment",
            "aging_potential_years",
            "similarity"
        ]
    ]
)
# Bloque adicional: explicación de por qué se recomienda cada vino, basado en su perfil sensorial y las características del vino.
print("\n--- Explicación de las recomendaciones ---")
for _, row in recomendadas.iterrows():
    explicacion = explain_recommendation(row, user_vector)
    print(f"- {row['varietal']} ({row['country']}): {explicacion}")


# 5. Más recomendaciones (simula botón "Mostrar más")
mas_recomendadas = recommend_wines(
    df,
    features,
    user_vector,
    extend=True
)

# Solo mostrar las NUEVAS (posiciones 4 a 8)
solo_nuevas = mas_recomendadas.iloc[3:8]

print("\n--- Más recomendaciones para tu perfil ---")
print(
    solo_nuevas[
        [
            "varietal",
            "country",
            "alcohol_pct",
            "rating",
            "price_segment",
            "aging_potential_years",
            "similarity"
        ]
    ]
)

# Explicación de por qué se recomiendan estas opciones adicionales, basada en su perfil sensorial y las características del vino.
print("\n--- Explicación de recomendaciones adicionales ---")
for _, row in solo_nuevas.iterrows():
    explicacion = explain_recommendation(row, user_vector)
    print(f"- {row['varietal']} ({row['country']}): {explicacion}")