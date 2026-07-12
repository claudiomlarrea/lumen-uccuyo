"""Estilos LUMEN — paleta alineada a EvaluAR (verde institucional)."""

# Misma familia cromática que EvaluAR
VERDE = "#044A30"
VERDE_OSCURO = "#033824"
VERDE_CLARO = "#D5E9E2"
VERDE_SIDEBAR = "#C6E0D6"
BORDE = "#B8D4C8"
ROJO = "#8B1E2D"
ORO = "#C4922A"
TEXTO = "#0f172a"
GRIS = "#475569"
FONDO = "#D5E9E2"
BLANCO = "#FFFFFF"


def css() -> str:
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Cormorant+Garamond:wght@600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Montserrat', sans-serif;
        font-size: 15px;
        color: {TEXTO};
    }}

    .stApp,
    [data-testid="stAppViewContainer"] {{
        background-color: {FONDO} !important;
    }}
    [data-testid="stHeader"] {{
        background-color: {FONDO} !important;
    }}
    [data-testid="stToolbar"] {{
        background-color: transparent !important;
    }}

    /* Contenido centrado con ancho cómodo (evita texto pegado a la izquierda en layout wide) */
    .main .block-container {{
        max-width: 1100px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}

    section[data-testid="stMain"] h1 {{
        color: {VERDE} !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        line-height: 1.25 !important;
    }}
    section[data-testid="stMain"] h2 {{
        color: {TEXTO} !important;
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        line-height: 1.3 !important;
    }}
    section[data-testid="stMain"] h3 {{
        color: {TEXTO} !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        line-height: 1.35 !important;
    }}
    section[data-testid="stMain"] h4 {{
        color: {VERDE} !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }}
    section[data-testid="stMain"] p,
    section[data-testid="stMain"] li,
    section[data-testid="stMain"] label {{
        color: {TEXTO};
        font-size: 0.95rem;
        line-height: 1.45;
    }}
    section[data-testid="stMain"] .stCaption,
    section[data-testid="stMain"] [data-testid="stCaptionContainer"] {{
        color: {GRIS} !important;
        font-size: 0.88rem !important;
    }}

    /* Sidebar — verde menta suave (como EvaluAR) */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div:first-child {{
        background-color: {VERDE_SIDEBAR} !important;
    }}
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
        color: {TEXTO} !important;
    }}
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {{
        background-color: {BLANCO};
    }}
    section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][aria-current="page"],
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] {{
        background-color: rgba(4, 74, 48, 0.12) !important;
        border-radius: 0.5rem;
    }}

    /* Alertas */
    div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {{
        color: inherit !important;
    }}
    .stAlert {{
        border-radius: 0.5rem;
    }}

    details[data-testid="stExpander"] {{
        background-color: {BLANCO} !important;
        border: 1px solid {BORDE};
        border-radius: 0.5rem;
    }}
    details[data-testid="stExpander"] summary {{
        background-color: {BLANCO} !important;
    }}

    /* Métricas compactas — evita el número gigante desalineado */
    div[data-testid="stMetric"] {{
        background-color: {BLANCO} !important;
        border: 1px solid {BORDE};
        border-radius: 0.5rem;
        padding: 0.75rem 1rem !important;
    }}
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] {{
        font-size: 0.85rem !important;
        color: {GRIS} !important;
    }}
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: {VERDE} !important;
        line-height: 1.2 !important;
    }}
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {{
        font-size: 0.85rem !important;
    }}

    /* Inputs y tabs más legibles */
    .stSelectbox label,
    .stTextInput label,
    .stTextArea label,
    .stDateInput label,
    .stNumberInput label,
    .stMultiSelect label {{
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }}
    div[data-testid="stTabs"] button[data-baseweb="tab"] {{
        font-size: 0.92rem !important;
        font-weight: 600 !important;
    }}

    .lumen-hero {{
        display: flex;
        gap: 1.2rem;
        align-items: center;
        padding: 1rem 1.25rem;
        background: {BLANCO};
        border: 1px solid {BORDE};
        border-left: 6px solid {VERDE};
        border-radius: 12px;
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 24px rgba(4, 74, 48, 0.08);
    }}
    .lumen-hero h1 {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.1rem !important;
        color: {VERDE} !important;
        margin: 0;
        line-height: 1.1;
    }}
    .lumen-hero p {{
        margin: 0.25rem 0 0 0;
        color: {GRIS} !important;
        font-size: 0.95rem;
    }}
    .lumen-badge {{
        display: inline-block;
        background: {ORO};
        color: {BLANCO};
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        padding: 0.2rem 0.55rem;
        border-radius: 999px;
        margin-bottom: 0.35rem;
    }}
    .lumen-note {{
        background: #FFF8E8;
        border: 1px solid #E8D5A3;
        border-left: 5px solid {ORO};
        padding: 0.85rem 1rem;
        border-radius: 8px;
        margin: 0.8rem 0 1.2rem 0;
        color: {TEXTO} !important;
        font-size: 0.92rem;
    }}
    .lumen-card {{
        background: {BLANCO};
        border: 1px solid {BORDE};
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.8rem;
    }}
    .lumen-card h4 {{
        margin: 0 0 0.35rem 0;
        color: {VERDE} !important;
        font-size: 1.05rem !important;
    }}
    .lumen-meta {{
        color: {GRIS} !important;
        font-size: 0.85rem;
    }}
    .lumen-footer {{
        margin-top: 2rem;
        padding-top: 0.8rem;
        border-top: 1px solid {BORDE};
        color: {GRIS} !important;
        font-size: 0.82rem;
        text-align: center;
    }}

    /* Botones — verde institucional con texto blanco */
    section[data-testid="stMain"] [data-testid="stButton"] button,
    section[data-testid="stMain"] .stButton button,
    section[data-testid="stMain"] .stDownloadButton button,
    section[data-testid="stMain"] [data-testid="stFormSubmitButton"] button,
    section[data-testid="stMain"] [data-testid="stBaseButton-primary],
    section[data-testid="stMain"] [data-testid="stBaseButton-secondary],
    section[data-testid="stMain"] button[kind="primary"],
    section[data-testid="stMain"] button[kind="secondary"],
    section[data-testid="stMain"] button[kind="primaryFormSubmit"],
    section[data-testid="stMain"] button[kind="secondaryFormSubmit"] {{
        background-color: {VERDE} !important;
        background: {VERDE} !important;
        color: {BLANCO} !important;
        border: 1px solid {VERDE} !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        box-shadow: none !important;
    }}
    section[data-testid="stMain"] [data-testid="stButton"] button *,
    section[data-testid="stMain"] .stButton button *,
    section[data-testid="stMain"] .stDownloadButton button *,
    section[data-testid="stMain"] [data-testid="stFormSubmitButton"] button *,
    section[data-testid="stMain"] [data-testid="stBaseButton-primary"] *,
    section[data-testid="stMain"] [data-testid="stBaseButton-secondary"] * {{
        color: {BLANCO} !important;
    }}
    section[data-testid="stMain"] [data-testid="stButton"] button:hover,
    section[data-testid="stMain"] [data-testid="stButton"] button:focus,
    section[data-testid="stMain"] [data-testid="stButton"] button:active,
    section[data-testid="stMain"] .stButton button:hover,
    section[data-testid="stMain"] .stButton button:focus,
    section[data-testid="stMain"] .stButton button:active,
    section[data-testid="stMain"] .stDownloadButton button:hover,
    section[data-testid="stMain"] .stDownloadButton button:focus,
    section[data-testid="stMain"] .stDownloadButton button:active,
    section[data-testid="stMain"] [data-testid="stFormSubmitButton"] button:hover,
    section[data-testid="stMain"] [data-testid="stFormSubmitButton"] button:focus,
    section[data-testid="stMain"] [data-testid="stFormSubmitButton"] button:active,
    section[data-testid="stMain"] [data-testid="stBaseButton-primary]:hover,
    section[data-testid="stMain"] [data-testid="stBaseButton-secondary]:hover {{
        background-color: {VERDE_OSCURO} !important;
        background: {VERDE_OSCURO} !important;
        color: {BLANCO} !important;
        border-color: {VERDE_OSCURO} !important;
    }}
    </style>
    """
