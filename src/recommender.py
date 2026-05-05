from src.similarity import compute_similarity, SIMILARITY_THRESHOLD

def recommend_wines(df, feature_matrix, user_vector, extend=False):
    """
    Devuelve recomendaciones ordenadas por similitud.
    - Por defecto: top 3
    - extend=True: hasta 8 (3 + 5)
    """
    similarities = compute_similarity(user_vector, feature_matrix)

    df = df.copy()
    df["similarity"] = similarities

    # Regla dura: solo vinos que cumplan el umbral
    filtered = df[df["similarity"] >= SIMILARITY_THRESHOLD]

    # Orden por similitud descendente
    ranked = filtered.sort_values("similarity", ascending=False)

    if extend:
        return ranked.head(8)

    return ranked.head(3)