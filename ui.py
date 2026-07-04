"""Componentes visuales compartidos de LUMEN."""

from __future__ import annotations

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from styles import css

ROOT = Path(__file__).resolve().parent
LOGO = ROOT / "assets" / "logo_uccuyo.png"
LOGO_BADGE = ROOT / "assets" / "logo_uccuyo_badge.png"

MIME_DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def guardar_word_para_descarga(data: bytes, file_name: str, *, dl_key: str) -> None:
    """Guarda el Word en sesión para el botón de descarga (patrón Consejo de Investigación)."""
    st.session_state[f"lumen_od_{dl_key}"] = {"bytes": data, "name": file_name}


def mostrar_descarga_word(dl_key: str) -> None:
    """Muestra botón de descarga .docx vía Streamlit (funciona en Streamlit Cloud)."""
    payload = st.session_state.get(f"lumen_od_{dl_key}")
    if not payload:
        return

    data = payload["bytes"]
    file_name = payload["name"]

    st.success(f"Documento **{file_name}** generado correctamente.")
    st.download_button(
        f"Descargar Word — {file_name}",
        data=data,
        file_name=file_name,
        mime=MIME_DOCX,
        key=f"dl_word_{dl_key}",
        type="primary",
        use_container_width=True,
    )
    st.caption("El archivo debe terminar en **.docx** y abrirse con Microsoft Word.")


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
    st.set_page_config(page_title=title, page_icon=str(LOGO) if LOGO.exists() else icon, layout="wide")
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
