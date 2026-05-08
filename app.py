import streamlit.components.v1 as components
import streamlit as st
import time

if "mode" not in st.session_state:
    st.session_state.mode = None

from src.analytics import plot_radar_chart
from src.explainability import explain_recommendation
from src.pairing import suggest_pairing
from src.pairing import render_pairing_screen

# =========================================================
# IMPORT DEL LOGO
# =========================================================
import base64
from pathlib import Path

def load_logo_base64(path: str) -> str:
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

LOGO_BASE64 = load_logo_base64("static/logo.png")

from src.load_data import load_wine_data
from src.preprocess import build_feature_matrix, add_wine_type
from src.recommender import recommend_wines
from src.explainability import explain_recommendation
from src.user_input import build_user_vector

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================
st.set_page_config(
    page_title="Sommelier Digital",
    page_icon="🍷",
    layout="centered"
)

# Carga de tipografías (solo una vez)
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500&family=Cedarville+Cursive&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)
# =========================================================
# SPLASH SCREEN (fade in / fade out)
# =========================================================

placeholder = st.empty()

if "show_intro" not in st.session_state:
    st.session_state.show_intro = True

if st.session_state.show_intro:

    placeholder.markdown(f"""
    <div style="
        position:fixed;
        top:0;
        left:0;
        width:100%;
        height:100%;
        background-color:black;
        display:flex;
        justify-content:center;
        align-items:center;
        flex-direction:column;
        animation: fadeOut 3s forwards;
        z-index:9999;
    ">
        <img src="data:image/png;base64,{LOGO_BASE64}" style="width:560px;"/>
        <div style="
            font-family: 'Playfair Display', serif;
            font-size:42px;
            color:#e6d8b5;
            margin-top:20px;
        ">
            Sommelier Digital
        </div>
    </div>

    <style>
    @keyframes fadeOut {{
        0% {{ opacity:1; }}
        70% {{ opacity:1; }}
        100% {{ opacity:0; visibility:hidden; }}
    }}
    </style>
    """, unsafe_allow_html=True)

    time.sleep(1)
    st.session_state.show_intro = False
    st.rerun()


# =========================================================
# Botonera de Inicio
# =========================================================
if st.session_state.mode is None:

    components.html("""
        <div style="text-align: center;">

            <div style="
                font-size: 42px;
                font-weight: 700;
                color: #e6d8b5;
                font-family: 'Playfair Display', serif;
                line-height: 1.05;
            ">
                🍷 Sommelier Digital
            </div>

            <div style="
                font-size: 20px;
                font-style: italic;
                color: #b0b0b0;
                margin-top: 2px;
                margin-bottom: 2px;
            ">
                Descubrí vinos acorde a lo que querés experimentar hoy…
            </div>

        </div>
        """, height=90)

    st.markdown("---")
    

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🍷 Descubrí tu vino a través de los sentidos"):
            st.session_state.mode = "sensory"
            st.rerun()

    with col2:
        if st.button("🍽️ Encontrá el vino para lo que vas a degustar"):
            st.session_state.mode = "pairing"
            st.rerun()


    st.markdown("---")

    st.markdown("""
        <div style="text-align: justify; text-align-last: left; max-width: 700px; margin: auto; 
                    font-size: 16px; color: #b0b0b0;">

        Sommelier Digital es una aplicación de recomendación de vinos basada en perfil sensorial. 
        El usuario define cómo quiere que se sienta el vino en boca y qué aromas busca.
        Nuestro Sommelier Digital sugiere vinos coherentes con esa experiencia, explicando 
        el razonamiento con lenguaje propio de un Sommelier.
        <i>Ofrece una función de maridaje inverso, donde el usuario describe 
        las características de su plato y el sistema recomienda vinos que armonizan con él.</i><br>

        Esta app fue desarrollada por Federico H. (para su Trabajo de Curso de Data Science I°) y Enólogos Profesionales, 
        combinando análisis de datos, machine learning y conocimiento enología para crear una experiencia única de descubrimiento Bacanal.<br><br>

        <i>¡Salud!</i><br>

        🍷 <i>Agradecimientos especiales a los Enólogos que aportaron su expertise y grandes conocimientos: 
        Ornella y Ezequiel.</i>🍷
        </div>
        """, unsafe_allow_html=True)


    st.markdown("---")

    st.stop()


if st.session_state.mode == "sensory":

# =========================================================
# ESCALAS SEMÁNTICAS
# =========================================================
    SCALES = {
        "acidity": {
            1: ("Suave", "Acidez baja, redondeada y apenas perceptible. Boca amable, sin tensión."),
            2: ("Delicada", "Acidez pulida y discreta, frescura sutil."),
            3: ("Equilibrada", "Acidez justa, fresca y armónica."),
            4: ("Vivaz", "Acidez marcada, expresiva y dinámica."),
            5: ("Vibrante", "Acidez filosa y electrizante, muy refrescante."),
        },
        "sweetness": {
            1: ("Muy seco", "Total ausencia de dulzor perceptible."),
            2: ("Seco", "Perfil limpio, sin dulzor dominante."),
            3: ("Equilibrado", "Dulzor sutil y bien integrado."),
            4: ("Meloso", "Dulzor envolvente y amable."),
            5: ("Goloso", "Dulzor marcado y seductor."),
        },
        "tannin": {
            1: ("Sedosos", "Taninos suaves y aterciopelados."),
            2: ("Pulidos", "Taninos finos y bien trabajados."),
            3: ("Integrados", "Taninos equilibrados y elegantes."),
            4: ("Firmes", "Taninos con carácter y estructura."),
            5: ("Intensos", "Taninos potentes y dominantes."),
        },
        "body": {
            1: ("Liviano", "Cuerpo ligero y etéreo."),
            2: ("Delgado", "Cuerpo fluido y fácil de beber."),
            3: ("Medio", "Buena presencia y balance."),
            4: ("Concentrado", "Cuerpo amplio y envolvente."),
            5: ("Potente", "Cuerpo robusto y profundo."),
        },
        "persistence": {
            1: ("Efímera", "Final muy corto y discreto."),
            2: ("Corta", "Final breve y claro."),
            3: ("Media", "Persistencia equilibrada."),
            4: ("Larga", "Final expresivo y placentero."),
            5: ("Muy larga", "Final prolongado y memorable."),
        },
        "complexity": {
            1: ("Directa", "Perfil simple y franco."),
            2: ("Sutil", "Capas leves y delicadas."),
            3: ("Armónica", "Equilibrio claro y rico."),
            4: ("Compleja", "Múltiples capas sensoriales."),
            5: ("Profunda", "Gran profundidad y expresión."),
        },
    }

    # =========================================================
    # HEADER PRINCIPAL
    # =========================================================
    st.title("🍷 Sommelier Digital")
    st.markdown(
        "<p style='font-size:20px; font-style:italic; color:#b0b0b0;'>Descubrí vinos acorde a lo que querés experimentar hoy…</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    if st.button("← Volver"):
            st.session_state.mode = None
            st.rerun()
    st.markdown("---")

    # =========================================================
    # PERFIL DE BOCA
    # =========================================================
    st.title("Perfil de Boca")

    def slider_with_description(title, key):
        st.markdown(f"### **{title}**")
        value = st.slider(
            label=title,
            min_value=1,
            max_value=5,
            value=3,
            key=key,
            label_visibility="collapsed"
        )
        word, description = SCALES[key][value]
        st.markdown(f"*{word} ({value}) — {description}*")
        st.markdown("")
        return value


    acidity = slider_with_description("Acidez · de suave a vibrante", "acidity")
    sweetness = slider_with_description("Dulzor · de seco a goloso", "sweetness")
    tannin = slider_with_description("Taninos · de sedosos a intensos", "tannin")
    body = slider_with_description("Cuerpo · de liviano a potente", "body")
    persistence = slider_with_description("Persistencia · de corta a muy larga", "persistence")
    complexity = slider_with_description("Complejidad · de directa a profunda", "complexity")

    # =========================================================
    # Función de Sugerencias del Sommelier Digital
    # =========================================================
    def suggest_wine_types(acidity, sweetness, tannin, body):
        suggestions = []

        # Tinto
        if tannin >= 3 or body >= 4:
            suggestions.append("Tinto")

        # Blanco
        if acidity >= 4 and tannin <= 2:
            suggestions.append("Blanco")

        # Rosé
        if acidity >= 4 and body <= 3:
            suggestions.append("Rosé")

        # Naranjo
        if tannin >= 3 and acidity >= 3:
            suggestions.append("Naranjo")

        # Espumante
        if acidity >= 4 and sweetness <= 3:
            suggestions.append("Espumante")

        # Dulce
        if sweetness >= 4:
            suggestions.append("Dulce")

        return list(set(suggestions))

    # =========================================================
    # TIPO DE VINO (selector + sugerencia)
    # =========================================================
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Tipo de vino")

        WINE_TYPES = [
            "Tinto",
            "Blanco",
            "Rosé",
            "Naranjo",
            "Espumante",
            "Fortificado (Oporto, Jerez)",
            "Dulce"
        ]

        selected_types = st.multiselect(
            "Seleccioná uno o más tipos de vino:",
            options=WINE_TYPES,
            default=WINE_TYPES # todos seleccionados por defecto
        )

    with col2:
        st.markdown("### Nuestra Sugerencia")

        suggested = suggest_wine_types(
            acidity, sweetness, tannin, body
        )

        if suggested:
            for s in suggested:
                st.markdown(f"🍷 {s}")
        else:
            st.markdown("—")

    # =========================================================
    # AROMAS
    # =========================================================
    st.subheader("Aromas deseados")
    st.caption("Podés elegir hasta tres aromas.")

    AROMA_OPTIONS = [
        "fruta roja",
        "fruta negra",
        "fruta blanca / amarilla",
        "floral",
        "herbal",
        "especias",
        "madera",
        "mineral",
    ]

    if "aromas_selected" not in st.session_state:
        st.session_state.aromas_selected = []

    selected = []

    col1, col2 = st.columns(2)
    for aroma in AROMA_OPTIONS[:4]:
        if col1.checkbox(aroma.capitalize(), aroma in st.session_state.aromas_selected):
            selected.append(aroma)

    for aroma in AROMA_OPTIONS[4:]:
        if col2.checkbox(aroma.capitalize(), aroma in st.session_state.aromas_selected):
            selected.append(aroma)

    if len(selected) > 3:
        st.warning("Elegí hasta tres aromas.")
        selected = selected[:3]

    st.session_state.aromas_selected = selected
    aromas = selected

    # =========================================================
    # ESTADOS
    # =========================================================
    st.session_state.setdefault("base_recommendations", None)
    st.session_state.setdefault("extended_recommendations", None)
    st.session_state.setdefault("show_more", False)
    st.session_state.setdefault("user_vector", None)

    # =========================================================
    # BOTÓN PRINCIPAL (DESHABILITADO SI YA HAY RESULTADOS)
    # =========================================================
    suggest_clicked = st.button(
        "Sugerir vinos para este perfil 🍷",
        disabled=st.session_state.base_recommendations is not None
    )

    if suggest_clicked:
        st.session_state.show_more = False

        with st.spinner("Buscando vinos que dialoguen con tu perfil sensorial…"):
            df = load_wine_data()
            df = add_wine_type(df)
            df = df[df["type"].isin(selected_types)]  # filtro Type
            features = build_feature_matrix(df)

            st.session_state.user_vector = build_user_vector(
                acidity=acidity,
                sweetness=sweetness,
                tannin=tannin,
                body=body,
                persistence=persistence,
                complexity=complexity,
                aromas_selected=aromas
            )

            all_reco = recommend_wines(
                df, features, st.session_state.user_vector, extend=True
            )

            # ✅ CONTROL DE CANTIDAD DE RESULTADOS
            if len(all_reco) == 0:
                st.warning("No encontramos variedades disponibles para el perfil y tipos seleccionados. Probá ampliando el filtro o modificando el perfil.")
                
                if suggested: #Sugerencias del Sommelier ante resutado cero
                    st.info("💡 Según tu perfil podrías explorar:")
                    for s in suggested:
                        st.markdown(f"🍷 {s}")
                    
                    # BOTÓN PARA APLICAR SUGERENCIA
                    if st.button("Usar sugerencia del Sommelier Digital 🍷"):
                        selected_types = suggested
                        st.rerun()
        
                st.stop()

            if len(all_reco) < 3:
                st.warning("Hay pocos vinos disponibles para el perfil y tipos seleccionados. Mostrando las mejores coincidencias disponibles.")

            st.session_state.base_recommendations = all_reco.iloc[:3]
            st.session_state.extended_recommendations = all_reco.iloc[3:8]

    # =========================================================
    # RENDER PRIMERAS 3
    # =========================================================
    if st.session_state.base_recommendations is not None:

        st.markdown("### Vinos que reflejan tu perfil sensorial")
        st.success("Perfil analizado. Estas son las expresiones que mejor lo representan.")
        st.caption(
            "Estas primeras etiquetas son las que mejor expresan el equilibrio entre tu perfil de boca y los aromas que seleccionaste."
        )

        for _, row in st.session_state.base_recommendations.iterrows():
            st.markdown(f"**{row['varietal']} ({row['type']}) — {row['country']}**")
            st.markdown(
                f"- Alcohol: {row['alcohol_pct']}%  \n"
                f"- Puntaje: {row['rating']} pts  \n"
                f"- Segmento: {row['price_segment']}  \n"
                f"- Guarda potencial: {row['aging_potential_years']} años"
            )
            
            st.caption(
                explain_recommendation(row, st.session_state.user_vector)
            )

            # 🍽️ Maridaje x vino
            pairings = suggest_pairing(row)

            st.markdown("🍽️ **Maridaje sugerido:**")
            pairing_text = " · ".join(pairings[:6]) 
            st.markdown(
                f"<span style='color:#9aa0a6; font-style:italic;'>{pairing_text}</span>",
                unsafe_allow_html=True
            )


            fig = plot_radar_chart(row, st.session_state.user_vector)
            
            # Guarda la figura en un buffer de memoria para evitar problemas de renderizado en Streamlit Cloud
            import io

            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
            buf.seek(0)


            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:

                st.image(buf, width=300)


            st.markdown("---")

        st.markdown(
            "_Si querés seguir explorando este perfil, hay más vinos que también podrían sorprenderte._"
        )

        if st.button(
            "Ver más opciones para este perfil 🍷",
            disabled=st.session_state.show_more
        ):
            st.session_state.show_more = True

    # =========================================================
    # RENDER EXTENDIDO
    # =========================================================
    if st.session_state.show_more and st.session_state.extended_recommendations is not None:
        st.markdown("---")
        st.markdown("### Más opciones alineadas con tu perfil")
        st.caption(
            "Estos vinos comparten el mismo espíritu sensorial, con matices que pueden abrir nuevas interpretaciones del perfil que buscás."
        )

        for _, row in st.session_state.extended_recommendations.iterrows():
            st.markdown(f"**{row['varietal']} ({row['type']}) — {row['country']}**")
            st.markdown(
                f"- Alcohol: {row['alcohol_pct']}%  \n"
                f"- Puntaje: {row['rating']} pts  \n"
                f"- Segmento: {row['price_segment']}  \n"
                f"- Guarda potencial: {row['aging_potential_years']} años"
            )
            st.caption(
                explain_recommendation(row, st.session_state.user_vector)
            )

            # 🍽️ Maridaje x vino (+ recomendaciones )
            pairings = suggest_pairing(row)

            st.markdown("🍽️ **Maridaje sugerido:**")
            pairing_text = " · ".join(pairings[:6])  
            st.markdown(
                f"<span style='color:#9aa0a6; font-style:italic;'>{pairing_text}</span>",
                unsafe_allow_html=True
            )



            st.markdown("---")

if st.session_state.mode == "pairing":
    render_pairing_screen()



