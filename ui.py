"""Componentes visuales compartidos de LUMEN."""

from __future__ import annotations

import base64
import html
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from styles import VERDE, VERDE_OSCURO, css

ROOT = Path(__file__).resolve().parent
LOGO = ROOT / "assets" / "logo_uccuyo.png"
LOGO_BADGE = ROOT / "assets" / "logo_uccuyo_badge.png"

MIME_DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def preparar_descarga_word(doc_bytes: bytes, file_name: str, *, dl_key: str) -> None:
    """Guarda el Word en sesión para descargarlo desde el navegador (Edge / Windows)."""
    st.session_state[f"lumen_od_{dl_key}"] = {
        "bytes": doc_bytes,
        "name": file_name,
    }


def mostrar_descarga_word(dl_key: str) -> None:
    """Descarga .docx vía JavaScript — no usa /media/ de Streamlit (evita UUID en Edge)."""
    payload = st.session_state.get(f"lumen_od_{dl_key}")
    if not payload:
        return

    file_name = payload["name"]
    b64 = base64.b64encode(payload["bytes"]).decode("ascii")

    st.success(f"Documento **{file_name}** generado correctamente.")

    components.html(
        f"""
        <div style="font-family: Montserrat, sans-serif;">
          <button type="button" id="lumen-dl-{dl_key}" style="
            width: 100%;
            padding: 0.75rem 1rem;
            background: {VERDE};
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
          ">Descargar Orden del Día</button>
          <p style="color: #5C6B63; font-size: 0.82rem; margin: 0.5rem 0 0 0;">
            Baja <strong>{html.escape(file_name)}</strong> (.docx) — compatible con Microsoft Edge.
          </p>
        </div>
        <script>
        (function () {{
          const fileName = {json.dumps(file_name)};
          const b64 = {json.dumps(b64)};
          const mime = {json.dumps(MIME_DOCX)};
          const btn = document.getElementById("lumen-dl-{dl_key}");
          btn.onmouseover = () => {{ btn.style.background = "{VERDE_OSCURO}"; }};
          btn.onmouseout = () => {{ btn.style.background = "{VERDE}"; }};
          btn.onclick = function () {{
            const raw = atob(b64);
            const bytes = new Uint8Array(raw.length);
            for (let i = 0; i < raw.length; i++) bytes[i] = raw.charCodeAt(i);
            const blob = new Blob([bytes], {{ type: mime }});
            const url = URL.createObjectURL(blob);
            const root = window.parent.document.body || document.body;
            const a = document.createElement("a");
            a.href = url;
            a.download = fileName;
            a.style.display = "none";
            root.appendChild(a);
            a.click();
            setTimeout(function () {{
              URL.revokeObjectURL(url);
              a.remove();
            }}, 200);
          }};
        }})();
        </script>
        """,
        height=95,
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
