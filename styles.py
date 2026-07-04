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

    html, body, [class*="css"] {{
        font-family: 'Montserrat', sans-serif;
        color: {TEXTO};
    }}

    .stApp {{
        background: linear-gradient(180deg, {VERDE_CLARO} 0%, {FONDO} 220px, {FONDO} 100%);
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: {VERDE_OSCURO};
    }}
    section[data-testid="stSidebar"] * {{
        color: {BLANCO} !important;
    }}
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {{
        background-color: rgba(255,255,255,0.12);
    }}
    /* Logo institucional sobre fondo claro en sidebar */
    .lumen-logo-wrap {{
        background: {BLANCO};
        border-radius: 14px;
        padding: 0.65rem 0.5rem;
        margin: 0.2rem auto 0.8rem auto;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0,0,0,0.18);
        max-width: 140px;
    }}
    .lumen-logo-wrap img {{
        width: 110px !important;
        margin: 0 auto;
    }}
    .lumen-logo-hero {{
        background: {BLANCO};
        border-radius: 16px;
        padding: 0.75rem;
        display: inline-block;
        box-shadow: 0 6px 18px rgba(0,77,44,0.12);
        border: 1px solid #d5e5db;
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
        color: {VERDE};
        margin: 0;
        line-height: 1.1;
    }}
    .lumen-hero p {{
        margin: 0.25rem 0 0 0;
        color: {GRIS};
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
        color: {TEXTO};
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
        color: {VERDE};
    }}
    .lumen-meta {{
        color: {GRIS};
        font-size: 0.85rem;
    }}
    .lumen-footer {{
        margin-top: 2rem;
        padding-top: 0.8rem;
        border-top: 1px solid #d5e5db;
        color: {GRIS};
        font-size: 0.82rem;
        text-align: center;
    }}
    a.lumen-dl-link {{
        display: block;
        text-align: center;
        padding: 0.75rem 1rem;
        background: {VERDE};
        color: {BLANCO} !important;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        margin: 0.5rem 0;
    }}
    a.lumen-dl-link:hover {{
        background: {VERDE_OSCURO};
        color: {BLANCO} !important;
    }}
    .lumen-dl-hint {{
        color: {GRIS};
        font-size: 0.82rem;
        margin: 0.35rem 0 0.75rem 0;
        word-break: break-all;
    }}
    div.stButton > button,
    div.stButton > button[kind="primary"],
    div.stButton > button[data-testid="baseButton-primary"],
    .stDownloadButton button,
    a[data-testid="stBaseLinkButton"],
    a[data-testid="stBaseLinkButton-secondary"] {{
        background: {VERDE} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px;
        font-weight: 600;
    }}
    div.stButton > button:hover,
    .stDownloadButton button:hover,
    a[data-testid="stBaseLinkButton"]:hover,
    a[data-testid="stBaseLinkButton-secondary"]:hover {{
        background: {VERDE_OSCURO} !important;
        color: white !important;
    }}
    </style>
    """
