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

# 🔥 NUEVO BLOQUE (frases dinámicas para pairing)
PAIRING_PHRASES = {

    "acidity_high": [
        "su acidez limpia el paladar entre bocados",
        "su frescura equilibra el conjunto",
        "aporta tensión y dinamismo al plato",
        "su acidez levanta la expresión del plato",
        "refresca y aligera la experiencia",
        "evita que el plato se vuelva pesado",
        "mantiene el conjunto vibrante",
        "resalta los matices del plato",
        "acompaña con frescura la preparación",
        "aporta energía al conjunto"
    ],

    "acidity_low": [
        "su perfil suave respeta la baja acidez del plato",
        "no introduce tensión innecesaria",
        "acompaña con una acidez contenida",
        "permite una experiencia más redonda",
        "mantiene la suavidad del conjunto",
        "se integra sin generar contraste ácido",
        "refuerza un perfil más amable",
        "acompaña una textura más envolvente",
        "no altera el equilibrio del plato",
        "sostiene una sensación más redondeada"
    ],

    "body_high": [
        "su cuerpo acompaña la intensidad del plato",
        "tiene estructura suficiente para sostener la preparación",
        "su volumen llena el paladar en línea con el plato",
        "acompaña la densidad del plato",
        "sostiene la intensidad general",
        "refuerza la presencia en boca",
        "su peso está bien alineado con el plato",
        "acompaña platos de mayor intensidad",
        "no queda desplazado frente al plato",
        "aporta consistencia al conjunto"
    ],

    "body_low": [
        "su ligereza respeta la delicadeza del plato",
        "acompaña sin imponerse",
        "mantiene una sensación fluida",
        "no satura el paladar",
        "permite que el plato se exprese",
        "acompaña con sutileza",
        "refuerza la liviandad del plato",
        "se integra con naturalidad",
        "no compite con la preparación",
        "mantiene equilibrio en boca"
    ],

    "complexity_high": [
        "su complejidad acompaña la riqueza del plato",
        "está a la altura de la elaboración",
        "dialoga con los matices del plato",
        "acompaña una propuesta más compleja",
        "refuerza la profundidad del plato",
        "ofrece capas que acompañan la experiencia",
        "se integra en platos elaborados",
        "acompaña múltiples matices",
        "sostiene la complejidad general",
        "aporta profundidad al conjunto"
    ],

    "complexity_low": [
        "su perfil directo respeta la sencillez del plato",
        "acompaña sin complejizar la experiencia",
        "mantiene una lectura simple y clara",
        "no introduce capas innecesarias",
        "se alinea con un plato más simple",
        "refuerza la claridad del conjunto",
        "acompaña sin distracciones",
        "mantiene un perfil accesible",
        "se integra con naturalidad",
        "respeta la pureza del plato"
    ],

    "general": [
        "logra un buen equilibrio con el perfil del plato",
        "se integra armónicamente en el conjunto",
        "acompaña de forma coherente",
        "funciona bien dentro del conjunto",
        "mantiene una buena armonía general",
        "encuentra balance con el plato",
        "acompaña sin desentonar",
        "se adapta al perfil del plato",
        "sostiene el equilibrio global",
        "acompaña de forma natural"
    ]
}

# agregamos context="sensory"
def explain_recommendation(row, user_vector, context="sensory"):
    parts = []

    # -------------------------
    # APERTURA / ROL
    # -------------------------
    intro_reasons = []

    if context == "sensory":

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

    else:  # 🍽️ MODO COMIDA

        reasons = []

        if user_vector is not None:

            if user_vector[0] >= 0.6 and row["acidity"] >= 4:
                reasons.append(random.choice(PAIRING_PHRASES["acidity_high"]))

            if user_vector[0] <= 0.4 and row["acidity"] <= 2:
                reasons.append(random.choice(PAIRING_PHRASES["acidity_low"]))

            if user_vector[3] >= 0.6 and row["body"] >= 4:
                reasons.append(random.choice(PAIRING_PHRASES["body_high"]))

            if user_vector[3] <= 0.4 and row["body"] <= 2:
                reasons.append(random.choice(PAIRING_PHRASES["body_low"]))

            if user_vector[5] >= 0.6 and row["complexity"] >= 4:
                reasons.append(random.choice(PAIRING_PHRASES["complexity_high"]))

            if user_vector[5] <= 0.4 and row["complexity"] <= 2:
                reasons.append(random.choice(PAIRING_PHRASES["complexity_low"]))

        if not reasons:
            reasons.append(random.choice(PAIRING_PHRASES["general"]))

        parts.append(
            "Este vino funciona muy bien con el perfil de tu plato porque "
            + " y ".join(reasons)
            + "."
        )

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