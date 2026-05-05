# Intento de explicar por qué se recomienda un vino específico a un usuario, basado en su perfil sensorial y las características del vino.
import random

# Estructura lógica del "fraseo" del Sommelier Digital: apertura variable → desarrollo sensorial → cierre evocativo.
# (Cualquier parecide con frases reales es casi coincidencia, me inspiré en algunos textos de sommeliers reales para darle un toque más auténtico).
OPENINGS = [
    "Este vino se integra naturalmente con tu perfil porque",
    "Dentro de la experiencia que buscás, este vino destaca porque",
    "Elegimos esta etiqueta ya que",
    "En línea con tu perfil sensorial, este vino se elige porque",
    "Este vino refleja con claridad el tipo de experiencia que definiste porque",
    "A partir de tu perfil, esta etiqueta resulta especialmente adecuada porque",
    "Este vino aparece como una buena interpretación de tu búsqueda sensorial porque",
    "Dentro de las expresiones posibles de tu perfil, este vino sobresale porque",
    "Este vino acompaña de forma coherente el perfil que elegiste porque",
    "En función de lo que valorás en copa, este vino se destaca porque",
]

NOSE_PHRASES = [
    "en nariz se expresa con",
    "la expresión aromática se apoya en",
    "aparecen capas de",
    "en el plano aromático se perciben",
    "la nariz propone una combinación de",
    "desde lo aromático se destacan",
    "en primera instancia aparecen",
    "el perfil aromático se construye a partir de",
    "la paleta aromática muestra",
    "en nariz se reconocen"
]

PALATE_PHRASES = [
    "en boca se muestra",
    "la estructura acompaña con",
    "deja una sensación de",
    "en boca se percibe",
    "la entrada en boca propone",
    "el paso por boca se caracteriza por",
    "la textura en boca resulta",
    "en el plano gustativo se expresa como",
    "la sensación en boca es de",
    "al recorrer el paladar se percibe"
]


CLOSINGS = [
    "Es un vino que invita a beber con atención.",
    "Se disfruta con calma, dejando que el vino se despliegue.",
    "Funciona muy bien cuando buscás equilibrio y presencia.",
    "Propone una experiencia franca, pero con matices.",
    "Acompaña momentos donde el disfrute está en los detalles.",
    "Es una expresión que se deja entender sin apuro.",
    "Invita a una degustación consciente, más allá del primer impacto.",
    "Se siente cómodo en contextos donde se valora la armonía.",
    "Ofrece una experiencia que crece a medida que avanza la copa.",
    "Resulta ideal cuando buscás un vino que acompañe sin imponerse."
]

ROLE_PHRASES = [
    "Dentro del conjunto de opciones, este vino cumple un rol más equilibrado",
    "Este vino aporta una lectura más directa del perfil que definiste",
    "Funciona como una versión más contenida del enfoque que buscás",
    "Dentro del perfil elegido, propone una interpretación más sobria",
]

BALANCE_PHRASES = [
    "no busca una expresión aromática dominante, sino un registro armónico",
    "se mueve en un plano aromático parejo y bien integrado",
    "prioriza coherencia y balance por sobre impacto aromático",
    "presenta un perfil aromático contenido, sin aristas sobresalientes",
]

EASE_PHRASES = [
    "en boca fluye de manera natural, sin imponer exigencias",
    "ofrece una experiencia amable y accesible",
    "se deja beber con naturalidad desde el primer sorbo",
    "acompaña sin generar resistencias al paladar",
]

STRUCTURAL_FEATURES = {
    "acidity": "acidez",
    "sweetness": "dulzor",
    "tannin": "taninos",
    "body": "cuerpo",
    "persistence": "persistencia",
    "complexity": "complejidad",
}

AROMA_FEATURES = {
    "aroma_red_fruit": "fruta roja",
    "aroma_black_fruit": "fruta negra",
    "aroma_white_yellow_fruit": "fruta blanca y amarilla",
    "aroma_floral": "floral",
    "aroma_spice": "especias",
    "aroma_wood": "madera",
    "aroma_mineral": "mineral",
    "aroma_herbal": "herbal",
}

def explain_recommendation(row, user_vector):
    parts = []

    # -------------------------
    # APERTURA / ROL
    # -------------------------
    intro_reasons = []

    if user_vector is not None:
        if user_vector[0] >= 0.6 and row["acidity"] >= 4:
            intro_reasons.append("acompaña tu búsqueda de frescura y tensión en boca")
        if user_vector[3] >= 0.6 and row["body"] >= 4:
            intro_reasons.append("sostiene la estructura y presencia que definiste")
        if user_vector[3] <= 0.4 and row["body"] <= 2:
            intro_reasons.append("refuerza una sensación de ligereza y fluidez")

    if intro_reasons:
        opening = random.choice(OPENINGS)
        parts.append(f"{opening} " + " y ".join(intro_reasons) + ".")
    else:
        parts.append(random.choice(ROLE_PHRASES) + ".")

    # -------------------------
    # NARIZ / EQUILIBRIO
    # -------------------------
    aromas = []

    if row.get("aroma_white_yellow_fruit", 0) == 1:
        aromas.append("fruta blanca y amarilla")
    if row.get("aroma_red_fruit", 0) == 1:
        aromas.append("fruta roja")
    if row.get("aroma_black_fruit", 0) == 1:
        aromas.append("fruta negra")
    if row.get("aroma_floral", 0) == 1:
        aromas.append("notas florales")
    if row.get("aroma_mineral", 0) == 1:
        aromas.append("matices minerales")
    if row.get("aroma_wood", 0) == 1:
        aromas.append("toques de madera")

    if aromas:
        nose_phrase = random.choice(NOSE_PHRASES)
        parts.append(f"{nose_phrase} " + ", ".join(aromas) + ".")
    else:
        parts.append(random.choice(BALANCE_PHRASES) + ".")

    # -------------------------
    # BOCA / FACILIDAD
    # -------------------------
    if row["persistence"] >= 4:
        palate_phrase = random.choice(PALATE_PHRASES)
        parts.append(
            f"{palate_phrase} un final persistente que acompaña la experiencia."
        )
    else:
        parts.append(random.choice(EASE_PHRASES) + ".")

    # -------------------------
    # CIERRE EVOCATIVO
    # -------------------------
    parts.append(random.choice(CLOSINGS))

    return " ".join(parts)