"""Estilos institucionales UCCuyo para el prototipo LUMEN."""

# Colores del Manual de Marcas (muestreados del emblema y aplicaciones)
VERDE = "#004D2C"
VERDE_OSCURO = "#003320"
VERDE_CLARO = "#E8F2EC"
ROJO = "#8B1E2D"
ORO = "#C4922A"
TEXTO = "#1A1A1A"
GRIS = "#5C6B63"
FONDO = "#F7FAF8"
BLANCO = "#FFFFFF"


def css() -> str:
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Cormorant+Garamond:wght@600;700&display=swap');

    .stApp {{
        background: linear-gradient(180deg, {VERDE_CLARO} 0%, {FONDO} 220px, {FONDO} 100%);
        font-family: 'Montserrat', sans-serif;
    }}

    /* Contenido principal — texto oscuro legible */
    section[data-testid="stMain"] {{
        color: {TEXTO};
    }}
    section[data-testid="stMain"] h1,
    section[data-testid="stMain"] h2,
    section[data-testid="stMain"] h3,
    section[data-testid="stMain"] h4,
    section[data-testid="stMain"] p,
    section[data-testid="stMain"] li,
    section[data-testid="stMain"] label,
    section[data-testid="stMain"] span {{
        color: {TEXTO};
    }}
    section[data-testid="stMain"] .stCaption,
    section[data-testid="stMain"] [data-testid="stCaptionContainer"] {{
        color: {GRIS} !important;
    }}

    /* Sidebar — solo la barra lateral en blanco */
    section[data-testid="stSidebar"] {{
        background: {VERDE_OSCURO};
    }}
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
        color: {BLANCO} !important;
    }}
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {{
        background-color: rgba(255,255,255,0.12);
    }}

    /* Alertas legibles */
    div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {{
        color: inherit !important;
    }}

    .lumen-hero {{
        display: flex;
        gap: 1.2rem;
        align-items: center;
        padding: 1rem 1.25rem;
        background: {BLANCO};
        border: 1px solid #d5e5db;
        border-left: 6px solid {VERDE};
        border-radius: 12px;
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 24px rgba(0,77,44,0.08);
    }}
    .lumen-hero h1 {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.1rem;
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
        border: 1px solid #d5e5db;
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.8rem;
    }}
    .lumen-card h4 {{
        margin: 0 0 0.35rem 0;
        color: {VERDE} !important;
    }}
    .lumen-meta {{
        color: {GRIS} !important;
        font-size: 0.85rem;
    }}
    .lumen-footer {{
        margin-top: 2rem;
        padding-top: 0.8rem;
        border-top: 1px solid #d5e5db;
        color: {GRIS} !important;
        font-size: 0.82rem;
        text-align: center;
    }}
    div.stButton > button,
    div.stButton > button[kind="primary"],
    .stDownloadButton button {{
        background: {VERDE} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px;
        font-weight: 600;
    }}
    div.stButton > button:hover,
    .stDownloadButton button:hover {{
        background: {VERDE_OSCURO} !important;
        color: white !important;
    }}
    </style>
    """
