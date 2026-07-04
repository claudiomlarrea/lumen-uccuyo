"""Componentes visuales compartidos de LUMEN."""

from __future__ import annotations

import base64
import html
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from styles import css

ROOT = Path(__file__).resolve().parent
LOGO = ROOT / "assets" / "logo_uccuyo.png"
LOGO_BADGE = ROOT / "assets" / "logo_uccuyo_badge.png"

MIME_DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def preparar_descarga_word(doc_bytes: bytes, file_name: str, *, dl_key: str) -> None:
    """Guarda el Word en sesión para descargarlo desde el navegador."""
    st.session_state[f"lumen_od_{dl_key}"] = {
        "bytes": doc_bytes,
        "name": file_name,
    }


def mostrar_descarga_word(dl_key: str) -> None:
    """Enlace directo en la página (no iframe): Edge respeta download=.docx."""
    payload = st.session_state.get(f"lumen_od_{dl_key}")
    if not payload:
        return

    file_name = payload["name"]
    b64 = base64.b64encode(payload["bytes"]).decode("ascii")
    safe_name = html.escape(file_name, quote=True)

    st.success(f"Documento **{file_name}** generado correctamente.")
    st.markdown(
        f"""
        <a href="data:{MIME_DOCX};base64,{b64}"
           download="{safe_name}"
           class="lumen-dl-link">Descargar Orden del Día</a>
        <p class="lumen-dl-hint">
          Un clic guarda <strong>{html.escape(file_name)}</strong> (.docx) en Descargas.
          Si Edge pregunta, elegí <em>Guardar</em>.
        </p>
        """,
        unsafe_allow_html=True,
    )


def _fijar_idioma_es() -> None:
    components.html(
        """
        <script>
            (function () {
                const doc = window.parent.document;
                doc.documentElement.lang = "es";
                doc.documentElement.setAttribute("translate", "no");
                if (doc.body) doc.body.setAttribute("translate", "no");
            })();
        </script>
        """,
        height=0,
        width=0,
    )


def setup_page(title: str, icon: str = "🌿") -> None:
    st.set_page_config(page_title=title, page_icon=icon, layout="wide")
    _fijar_idioma_es()
    st.markdown(css(), unsafe_allow_html=True)


def sidebar_brand(caption: str = "") -> None:
    with st.sidebar:
        if LOGO_BADGE.exists():
            st.image(str(LOGO_BADGE), width=130)
        elif LOGO.exists():
            st.image(str(LOGO), width=110)
        st.markdown("### LUMEN")
        st.caption("Orden del Día Institucional")
        if caption:
            st.caption(caption)
        st.markdown("---")
        st.caption("Prototipo de demostración")
        st.caption("No modifica planillas productivas")


def hero_logo(width: int = 120) -> None:
    if LOGO_BADGE.exists():
        st.image(str(LOGO_BADGE), width=width)
    elif LOGO.exists():
        st.image(str(LOGO), width=width)
