import streamlit as st
import plotly.express as px
import pandas as pd
import streamlit.components.v1 as components

def elegant_separator():
    st.markdown("""
        <div style="
            height: 1px;
            margin: 40px 0 30px 0;
            background: linear-gradient(to right, transparent, #444, transparent);
        "></div>
    """, unsafe_allow_html=True)


def render_comparative(df):

    st.title("🍇 Comparatívas de Varietales")
    st.markdown(
        "<p style='font-size:20px; font-style:italic; color:#b0b0b0;'>Conocé los varietales desde la comparativa</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    if st.button("← Volver"):
            st.session_state.mode = None
            st.rerun()
    st.markdown("---")


    # ===================================
    # Selector de Varietales
    # ===================================

    VARIETAL_TRANSLATIONS = {
        "Late harvest": "Cosecha tardía",
        "Orange Wine": "Naranjo"
    }

    # 1. obtener varietales únicos
    varietals = df["varietal"].dropna().unique()

    # 2. mapear a display
    display_mapping = {
        v: VARIETAL_TRANSLATIONS.get(v, v)
        for v in varietals
    }

    # 3. ordenar por el VALOR visible (clave del fix)
    def sort_key(item):
        return item[1]

    sorted_items = sorted(display_mapping.items(), key=sort_key)

    # 4. separar listas
    varietals_sorted = [item[0] for item in sorted_items]
    display_varietals = [item[1] for item in sorted_items]


    # 5. Reverse mapping (para volver al dataset original)
    reverse_translation = {
        v: k for k, v in VARIETAL_TRANSLATIONS.items()
    }

    # 6. Multiselect (LO QUE VE EL USUARIO)
    selected_display = st.multiselect(
        "Seleccioná hasta 5 varietales",
        options=display_varietals,
        max_selections=5
    )

    # 7. Convertir selección a valores reales del dataset
    selected_varietals = [
        reverse_translation[v] if v in reverse_translation else v
        for v in selected_display
    ]

    if not selected_varietals:
        st.warning("Seleccioná al menos un varietal")
        st.stop()

    if len(selected_varietals) == 1:
        st.info("Visualizando distribución de un solo varietal")

    df_filtered = df[df["varietal"].isin(selected_varietals)]

    if df_filtered.empty:
        st.warning("No hay datos para los varietales seleccionados")
        st.stop()

    # ===================================
    # FEATURES
    # ===================================
    FEATURE_TRANSLATIONS = {
        "acidity": "Acidez",
        "sweetness": "Dulzor",
        "tannin": "Taninos",
        "body": "Cuerpo",
        "complexity": "Complejidad",
        "persistence": "Persistencia",
        "alcohol_pct": "Alcohol (%)",
        "rating": "Puntaje"
    }

    SCALE_MEANINGS = {
        "acidity": {
            1: "Muy suave",
            2: "Delicada",
            3: "Equilibrada",
            4: "Vivaz",
            5: "Vibrante"
        },
        "body": {
            1: "Liviano",
            2: "Ligero",
            3: "Medio",
            4: "Concentrado",
            5: "Potente"
        },
        "tannin": {
            1: "Sedosos",
            2: "Pulidos",
            3: "Integrados",
            4: "Firmes",
            5: "Intensos"
        },
        "sweetness": {
            1: "Muy seco",
            2: "Seco",
            3: "Equilibrado",
            4: "Meloso",
            5: "Goloso"
        },
        "complexity": {
            1: "Directa",
            2: "Sutil",
            3: "Armónica",
            4: "Compleja",
            5: "Profunda"
        },
        "persistence": {
            1: "Efímera",
            2: "Corta",
            3: "Media",
            4: "Larga",
            5: "Muy larga"
        }
    }

    def interpret_wine_character(row):

        acidity = int(row["acidity"])
        body = int(row["body"])
        tannin = int(row["tannin"])
        sweetness = int(row["sweetness"])

        descriptors = []

        # ACIDEZ
        if acidity >= 4:
            descriptors.append("fresco")
        elif acidity <= 2:
            descriptors.append("suave")

        # CUERPO
        if body >= 4:
            descriptors.append("estructurado")
        elif body <= 2:
            descriptors.append("liviano")

        # TANINOS
        if tannin >= 4:
            descriptors.append("tánico")
        elif tannin <= 2:
            descriptors.append("suave")

        # DULZOR
        if sweetness >= 4:
            descriptors.append("goloso")
        elif sweetness <= 2:
            descriptors.append("seco")

        # fallback
        if not descriptors:
            descriptors.append("equilibrado")

        # frase final
        return "Carácter " + ", ".join(descriptors)

    def build_hover_text(row, x_axis, y_axis):

        x_val = round(row[x_axis])
        y_val = round(row[y_axis])

        x_label = FEATURE_TRANSLATIONS[x_axis]
        y_label = FEATURE_TRANSLATIONS[y_axis]

        x_meaning = SCALE_MEANINGS.get(x_axis, {}).get(x_val, "")
        y_meaning = SCALE_MEANINGS.get(y_axis, {}).get(y_val, "")

        character = interpret_wine_character(row)

        return (
            f"🍇 {row['varietal']}<br>"
            f"🌍 {row['country']} · Guarda: {row.get('aging_potential_years', 'N/A')} años<br><br>"
            f"{x_label}: {x_val} ({x_meaning})<br>"
            f"{y_label}: {y_val} ({y_meaning})<br><br>"
            f"🧠 <i>{character}</i>"
        )

    elegant_separator()

    # ===================================
    # Scatter
    # ===================================
    numeric_cols = [
        "acidity", "sweetness", "tannin", "body",
        "complexity", "persistence", "alcohol_pct", "rating"
    ]

    col1, col2 = st.columns(2)

    feature_options = {
        FEATURE_TRANSLATIONS[c]: c
        for c in numeric_cols
    }

    df_filtered["character"] = df_filtered.apply(
        lambda row: interpret_wine_character(row),
        axis=1
    )

    reverse_features = {v: k for k, v in FEATURE_TRANSLATIONS.items()}

    x_display = col1.selectbox("Eje X", list(feature_options.keys()), index=0)
    y_display = col2.selectbox("Eje Y", list(feature_options.keys()), index=3)

    x_axis = feature_options[x_display]
    y_axis = feature_options[y_display]

    st.markdown("### 🍷 Relación entre variables")

    st.caption(
        "Este gráfico muestra cómo se distribuyen los vinos según dos características elegidas. "
        "Cada punto representa un vino, permitiendo comparar estilos y detectar similitudes o diferencias entre varietales."
    )

    fig_scatter = px.scatter(
        df_filtered,
        x=x_axis,
        y=y_axis,
        color="varietal",
        custom_data=[
            "varietal",
            "country",
            "aging_potential_years",
            "character",
           
        ],
        labels={
            x_axis: FEATURE_TRANSLATIONS[x_axis],
            y_axis: FEATURE_TRANSLATIONS[y_axis],
            "varietal": "Varietal"
        }
    )

    fig_scatter.update_traces(
        hovertemplate=
        "<b>🍇 %{customdata[0]}</b><br>" +
        "🌍 %{customdata[1]} · Guarda: %{customdata[2]} años<br><br>" +

        f"{FEATURE_TRANSLATIONS[x_axis]}: %{{x}}<br>" +
        f"{FEATURE_TRANSLATIONS[y_axis]}: %{{y}}<br><br>" +

        "🍷 %{customdata[3]}<extra></extra>"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    def render_scale_legend(feature):
        if feature in SCALE_MEANINGS:
            labels = SCALE_MEANINGS[feature]
            text = " · ".join([f"{k}: {v}" for k, v in labels.items()])
            st.caption(f"📌 Escala de {FEATURE_TRANSLATIONS[feature]} → {text}")
    
    def render_scale_box(feature):

        if feature in SCALE_MEANINGS:

            labels = SCALE_MEANINGS[feature]

            text = "".join([
                f"<div style='margin-bottom:4px;'>• <b>{k}</b> — {v}</div>"
                for k, v in labels.items()
            ])

            title = FEATURE_TRANSLATIONS[feature]

            html = f"""<div style="
                background-color: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 10px;
                padding: 12px 16px 18px 16px;
                margin-top: 10px;
                margin-bottom: 10px;
                font-size: 14px;
                color: #cfcfcf;

                min-height: 140px;
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
            ">

                <div style="
                    font-size: 14px;
                    font-weight: 600;
                    margin-bottom: 6px;
                    color: #e6d8b5;
                ">
                    📌 Escala de {title}
                </div>

                <div style="line-height: 1.6;">
                    {text}
                </div>

            </div>
            """
            components.html(html, height=200)
            #st.markdown(html, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        render_scale_box(x_axis)

    with col2:
        render_scale_box(y_axis)

    elegant_separator()

    # ===================================
    # Boxplot
    # ===================================
    
    st.markdown("### 🍷 Distribución por característica")

    st.caption(
        "Este gráfico muestra cómo se distribuye cada varietal en una característica específica. "
        "Permite ver consistencia, variabilidad y valores extremos dentro de cada estilo de vino."
    )

    feature_display = st.selectbox(
        "Seleccioná característica",
        list(feature_options.keys()),
        key="box"
    )

    feature = feature_options[feature_display]

    fig_box = px.box(
        df_filtered,
        x="varietal",
        y=feature,
        color="varietal",
        title=f"Distribución de {feature_display} por varietal",
        labels={
            "varietal": "Varietal",
            feature: feature_display
        }
    )
    
    fig_box.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig_box, use_container_width=True)

    def generate_boxplot_insight(df, feature):

        grouped = df.groupby("varietal")[feature].mean()
        feature_name = FEATURE_TRANSLATIONS[feature]

        # ordenar
        sorted_means = grouped.sort_values(ascending=False)

        top = sorted_means.index[0]
        bottom = sorted_means.index[-1]

        # media global → CLAVE
        global_mean = grouped.mean()

        # distancia respecto a la media
        deviations = {
            v: grouped[v] - global_mean for v in grouped.index
        }

        # clasificar comportamiento
        above = [v for v, d in deviations.items() if d > 0.3]
        below = [v for v, d in deviations.items() if d < -0.3]
        aligned = [v for v, d in deviations.items() if abs(d) <= 0.3]

        # interpretación del conjunto
        spread = max(grouped) - min(grouped)

        if spread < 0.5:
            distribution = "muy homogénea, con escasa dispersión entre varietales"
        elif spread < 1.5:
            distribution = "moderadamente dispersa, con diferencias perceptibles"
        else:
            distribution = "heterogénea, con contrastes marcados entre estilos"

        # perfil sensorial según feature
        if feature == "acidity":
            profile = "frescura y tensión en boca"
            pairing = (
                "mayor acidez favorece el equilibrio con platos grasos o intensos, "
                "mientras que valores más bajos acompañan mejor preparaciones suaves"
            )
        elif feature == "body":
            profile = "estructura y peso en boca"
            pairing = (
                "mayor cuerpo se asocia a carnes rojas y platos contundentes, "
                "mientras que perfiles livianos funcionan mejor con opciones ligeras"
            )
        else:
            profile = "características estructurales del vino"
            pairing = "una selección de maridajes acorde a la intensidad del perfil"

        # construir lista
        comparison = ", ".join([
            f"{v} ({round(grouped[v],1)})"
            for v in sorted_means.index
        ])

        # insight final
        insight = (
            f"Desde el punto de vista de la media, {feature_name.lower()} define el eje central del perfil de los vinos seleccionados, "
            f"ubicándose en torno a un valor promedio de {round(global_mean,1)}. "
            
            f"La distribución de las medias entre varietales resulta {distribution}. "
            f"{top} se posiciona en el extremo superior, mientras que {bottom} marca el límite inferior, generando un rango de interpretación claro. "
            
            f"En relación a este punto central, se observa que {', '.join(above) if above else 'ningún varietal'} tiende a expresar valores por encima de la media, "
            f"aportando mayor intensidad, mientras que {', '.join(below) if below else 'ninguno'} se ubica por debajo, mostrando perfiles más moderados. "
            f"{', '.join(aligned) if aligned else 'Algunos varietales'} se alinean con el promedio, representando el comportamiento más típico del conjunto. "
            
            f"Sensorialmente, esto se traduce en {profile}, donde la posición relativa de cada varietal permite anticipar su comportamiento en boca. "
            
            f"Desde una perspectiva de decisión, esta lectura facilita la selección: aquellos por encima de la media serán más adecuados cuando se busque intensidad y contraste, "
            f"mientras que los alineados o por debajo favorecerán armonía y equilibrio con el plato. En términos de maridaje, {pairing}."
            
            f" La gradación completa entre varietales puede resumirse como: {comparison}."
        )

        return insight


    insight = generate_boxplot_insight(df_filtered, feature)

    html = f"""
    <div style="
        background-color: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 14px 18px 18px 18px;
        margin-top: 15px;
        margin-bottom: 10px;
        font-size: 14px;
        color: #cfcfcf;
    ">

        <div style="
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #e6d8b5;
        ">
            🍷 Comentario del Sommelier Digital
        </div>

        <div style="line-height: 1.6;">
            {insight}
        </div>

    </div>
    """

    components.html(html, height=390)


    elegant_separator()

    # ===================================
    # Barplot (promedios)
    # ===================================
    df_avg = (
        df_filtered
        .groupby("varietal")[numeric_cols]
        .mean()
        .reset_index()
    )

    st.markdown("### 🍷 Promedio por varietal")

    st.caption(
        "Este gráfico compara el valor promedio de una característica entre varietales. "
        "Es útil para identificar el perfil típico de cada estilo de vino."
    )

    feature_bar_display = st.selectbox(
        "Comparar promedio",
        list(feature_options.keys()),
        key="bar"
    )

    feature_bar = feature_options[feature_bar_display]

    fig_bar = px.bar(
        df_avg,
        x="varietal",
        y=feature_bar,
        color="varietal",
        title=f"Promedio de {feature_bar_display} por varietal",
        labels={
            "varietal": "Varietal",
            feature_bar: feature_bar_display
        }
    )

    fig_bar.update_layout(
        xaxis_tickangle=-45
    )

    def generate_barplot_insight(df_avg, feature):

        feature_name = FEATURE_TRANSLATIONS[feature]

        # ordenar
        sorted_df = df_avg.sort_values(by=feature, ascending=False)

        top = sorted_df.iloc[0]
        bottom = sorted_df.iloc[-1]

        # detectar bloques (alto / medio / bajo)
        values = sorted_df[feature]
        mean_val = values.mean()

        high = sorted_df[sorted_df[feature] > mean_val + 0.3]["varietal"].tolist()
        low = sorted_df[sorted_df[feature] < mean_val - 0.3]["varietal"].tolist()
        mid = sorted_df[
            (sorted_df[feature] >= mean_val - 0.3) &
            (sorted_df[feature] <= mean_val + 0.3)
        ]["varietal"].tolist()

        # interpretación sensorial
        if feature == "acidity":
            dimension = "frescura"
            high_desc = "más vibrantes y tensos"
            low_desc = "más redondeados y suaves"
            pairing_high = "platos grasos o intensos que necesiten contraste"
            pairing_low = "preparaciones delicadas o de baja intensidad"

        elif feature == "body":
            dimension = "estructura"
            high_desc = "más estructurados y contundentes"
            low_desc = "más ligeros y de trago fácil"
            pairing_high = "carnes rojas o platos de alta intensidad"
            pairing_low = "ensaladas, pescados o entradas ligeras"

        else:
            dimension = feature_name.lower()
            high_desc = "más intensos"
            low_desc = "más suaves"
            pairing_high = "platos de mayor intensidad"
            pairing_low = "platos más delicados"

        # construir insight
        insight = (
            f"Comparando los perfiles promedio de {feature_name.lower()}, se observa una diferenciación clara en términos de {dimension}. "
            
            f"{top['varietal']} se posiciona como la opción más {high_desc}, mientras que {bottom['varietal']} representa el extremo opuesto, con un perfil {low_desc}. "
            
            f"En términos prácticos, esto permite segmentar los varietales en estilos de consumo: "
            f"{', '.join(high) if high else 'ninguno'} destacan por su intensidad, "
            f"{', '.join(low) if low else 'ninguno'} por su suavidad, "
            f"y {', '.join(mid) if mid else 'algunos'} se ubican en un punto intermedio de equilibrio. "
            
            f"Desde el punto de vista del uso, los primeros resultan más adecuados para {pairing_high}, "
            f"mientras que los segundos funcionan mejor en {pairing_low}. "
            
            f"Esta lectura convierte el gráfico en una herramienta práctica de elección según ocasión, estilo de plato o preferencia personal."
        )

        return insight

    st.plotly_chart(fig_bar, use_container_width=True)

    insight = generate_barplot_insight(df_avg, feature_bar)

    html = f"""
    <div style="
        background-color: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 14px 18px 18px 18px;
        margin-top: 15px;
        margin-bottom: 10px;
        font-size: 14px;
        color: #cfcfcf;
    ">

        <div style="
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #e6d8b5;
        ">
            🍷 Consideraciones del Sommelier Digital
        </div>

        <div style="line-height: 1.6;">
            {insight}
        </div>

    </div>
    """

    components.html(html, height=280)

    elegant_separator()

    # ===================================
    # Heatmap
    # ===================================

    heatmap_original = df_avg.set_index("varietal").drop(columns=["rating"], errors="ignore")
    heatmap_scaled = heatmap_original.copy()
    
    st.markdown("### 🍷 Mapa de intensidad")

    st.caption(
        "Este mapa muestra la intensidad promedio de cada característica por varietal. "
        "Permite obtener una visión global y rápida de los perfiles sensoriales."
    )

    def get_varietal_role(row):

        acidity = row["acidity"]
        body = row["body"]
        tannin = row["tannin"]

        if body >= 3.5 or tannin >= 3.5:
            return "🍖 Estructural — ideal para carnes rojas, platos intensos o salsas concentradas"
        elif acidity >= 3.5:
            return "🍋 Fresco - ideal para platos grasos, fritos o que requieran contraste"
        elif body <= 2.5 and tannin <= 2.5:
            return "🪶 Suave — ideal para entradas ligeras, pescados o consumo informal"
        else:
            return "⚖️ Equilibrado — versátil, funciona bien con una amplia variedad de platos"

    role_map = {}
    for varietal in heatmap_original.index:
        role_map[varietal] = get_varietal_role(heatmap_original.loc[varietal])

    def scale_alcohol(value):
        min_val = 10
        max_val = 20
        return round(((value - min_val) / (max_val - min_val)) * 5, 2)

    def get_alcohol_label(value):
        if value < 12:
            return "Ligero"
        elif value < 13.5:
            return "Moderado"
        elif value < 14.5:
            return "Alto"
        else:
            return "Muy elevado"

    # aplicar escala SOLO al visual
    heatmap_scaled["alcohol_pct"] = heatmap_scaled["alcohol_pct"].apply(scale_alcohol)

    qualitative_matrix = []

    for varietal in heatmap_scaled.index:
        row_values = []

        for col in heatmap_scaled.columns:

            value_scaled = heatmap_scaled.loc[varietal, col]
            value_int = round(value_scaled)

            original_value = heatmap_original.loc[varietal, col]

            if col == "alcohol_pct":
                meaning = get_alcohol_label(original_value)  # ✅ FIX CLAVE
            else:
                meaning = SCALE_MEANINGS.get(col, {}).get(value_int, "")

            role = role_map[varietal]

            final_text = f"{meaning if meaning else '—'}<br>{role}"

            row_values.append(final_text)


        qualitative_matrix.append(row_values)

    heatmap_display = heatmap_scaled.round(2)
    heatmap_display.columns = [
        FEATURE_TRANSLATIONS[c] for c in heatmap_display.columns
    ]

    # TEXTO REAL (no escalado)
    text_matrix = heatmap_original.round(2).values


    fig_heatmap = px.imshow(
        heatmap_display,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Mapa de Intensidades por Varietal"
    )

    fig_heatmap.update_traces(
        text=text_matrix,                # ✅ valor real visible
        texttemplate="%{text}",
        customdata=qualitative_matrix,
        hovertemplate=
        "%{x}: %{text}<br><br>" +        # ✅ valor real en hover
        "🍇 %{y}<br><br>" +
        "%{customdata}<extra></extra>"
    )

    def generate_heatmap_insight(df_avg):

        df_clean = df_avg.drop(columns=["rating"], errors="ignore")

        # ✅ escalar alcohol también en insight
        df_clean["alcohol_pct"] = df_clean["alcohol_pct"].apply(scale_alcohol)

        profiles = []

        for _, row in df_clean.iterrows():

            varietal = row["varietal"]
            features = row.drop("varietal")

            sorted_features = features.sort_values(ascending=False)

            top_feature = sorted_features.index[0]
            second_feature = sorted_features.index[1]

            profiles.append(
                f"{varietal} presenta una identidad marcada por su {FEATURE_TRANSLATIONS[top_feature].lower()}, "
                f"complementada por una presencia destacada de {FEATURE_TRANSLATIONS[second_feature].lower()}"
            )

        profile_summary = ". ".join(profiles) + "."

        structured = df_clean[
            (df_clean["body"] + df_clean["tannin"]) >
            (df_clean["body"] + df_clean["tannin"]).mean()
        ]["varietal"].tolist()

        fresh = df_clean[
            df_clean["acidity"] > df_clean["acidity"].mean()
        ]["varietal"].tolist()

        style_summary = (
            f"A nivel de estilos, se observa una diferenciación clara: "
            f"{', '.join(structured) if structured else 'algunos varietales'} se orientan hacia perfiles más estructurados, "
            f"mientras que {', '.join(fresh) if fresh else 'otros'} privilegian la frescura y vivacidad."
        )

        balance_descriptions = []

        for _, row in df_clean.iterrows():

            varietal = row["varietal"]
            std_dev = row.drop("varietal").std()

            if std_dev < 0.5:
                text = f"{varietal} muestra una gran armonía interna entre sus componentes"
            elif std_dev < 1.5:
                text = f"{varietal} mantiene un equilibrio adecuado con leves variaciones entre atributos"
            else:
                text = f"{varietal} presenta contrastes notorios que le aportan complejidad estructural"

            balance_descriptions.append(text)

        balance_summary = ". ".join(balance_descriptions) + "."

        return (
            f"{profile_summary} {style_summary} En términos de balance, {balance_summary} "
            f"En conjunto, este mapa permite comprender tanto el carácter individual como el posicionamiento relativo de cada varietal."
        )

    # render
    st.plotly_chart(fig_heatmap, use_container_width=True)

    insight_heatmap = generate_heatmap_insight(df_avg)

    html = f"""
    <div style="
        background-color: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 14px 18px 18px 18px;
        margin-top: 15px;
        margin-bottom: 10px;
        font-size: 14px;
        color: #cfcfcf;
    ">
        <div style="
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #e6d8b5;
        ">
            🍷 Análisis del Sommelier Digital
        </div>

        <div style="line-height: 1.6;">
            {insight_heatmap}
        </div>

    </div>
    """

    components.html(html, height=400)


    elegant_separator()
    
    if st.button("← Volver"):
        st.session_state.mode = None
