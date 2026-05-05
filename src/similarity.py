from sklearn.metrics.pairwise import cosine_similarity

# Umbral aprobado por vos
SIMILARITY_THRESHOLD = 0.80

def compute_similarity(user_vector, wine_matrix):
    """
    Calcula la similitud coseno entre el perfil del usuario
    y todos los vinos del dataset.
    """
    similarities = cosine_similarity(
        user_vector.reshape(1, -1),
        wine_matrix
    )
    return similarities.flatten()
