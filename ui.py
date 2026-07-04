"""Componentes visuales compartidos de LUMEN."""

from __future__ import annotations

import base64
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from styles import VERDE, VERDE_OSCURO, css

ROOT = Path(__file__).resolve().parent
LOGO = ROOT / "assets" / "logo_uccuyo.png"
LOGO_BADGE = ROOT / "assets" / "logo_uccuyo_badge.png"

MIME_DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def _instalar_descarga_edge() -> None:
    """Listener en la ventana principal (Edge respeta el nombre .docx con Guardar como)."""
    components.html(
        f"""
        <script>
        (function () {{
            const topWin = window.top;
            if (topWin.__lumenWordDownloadReady) return;
            topWin.__lumenWordDownloadReady = true;

            topWin.addEventListener("message", async function (ev) {{
                const msg = ev.data;
                if (!msg || msg.type !== "lumen-word-download") return;

                const fileName = msg.fileName;
                const mime = msg.mime || {json.dumps(MIME_DOCX)};
                const raw = atob(msg.b64);
                const bytes = new Uint8Array(raw.length);
                for (let i = 0; i < raw.length; i++) bytes[i] = raw.charCodeAt(i);
                const blob = new Blob([bytes], {{ type: mime }});

                if (typeof topWin.showSaveFilePicker === "function") {{
                    try {{
                        const handle = await topWin.showSaveFilePicker({{
                            suggestedName: fileName,
                            types: [{{
                                description: "Documento Word",
                                accept: {{ [mime]: [".docx"] }},
                            }}],
                        }});
                        const writable = await handle.createWritable();
                        await writable.write(blob);
                        await writable.close();
                        return;
                    }} catch (err) {{
                        if (err && err.name === "AbortError") return;
                    }}
                }}

                const nav = topWin.navigator;
                if (typeof nav.msSaveOrSaveBlob === "function") {{
                    nav.msSaveOrSaveBlob(blob, fileName);
                    return;
                }}

                const url = URL.createObjectURL(blob);
                const a = topWin.document.createElement("a");
                a.href = url;
                a.download = fileName;
                topWin.document.body.appendChild(a);
                a.click();
                setTimeout(function () {{
                    URL.revokeObjectURL(url);
                    a.remove();
                }}, 500);
            }});
        }})();
        </script>
        """,
        height=0,
        width=0,
    )


def preparar_descarga_word(doc_bytes: bytes, file_name: str, *, dl_key: str) -> None:
    """Guarda el Word en sesión para descargarlo desde el navegador."""
    st.session_state[f"lumen_od_{dl_key}"] = {
        "bytes": doc_bytes,
        "name": file_name,
    }


def mostrar_descarga_word(dl_key: str) -> None:
    """Descarga Word en Edge/Windows: cuadro Guardar como con nombre .docx correcto."""
    payload = st.session_state.get(f"lumen_od_{dl_key}")
    if not payload:
        return

    file_name = payload["name"]
    b64 = base64.b64encode(payload["bytes"]).decode("ascii")

    st.success(f"Documento **{file_name}** generado correctamente.")
    st.caption(
        "Clic en **Descargar Orden del Día** → Edge abre **Guardar como** con el archivo `.docx`. "
        "Elegí Descargas (o Escritorio) y Guardar."
    )

    components.html(
        f"""
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
            font-family: Montserrat, sans-serif;
        ">Descargar Orden del Día</button>
        <script>
        (function () {{
            const btn = document.getElementById("lumen-dl-{dl_key}");
            btn.onmouseover = function () {{ btn.style.background = "{VERDE_OSCURO}"; }};
            btn.onmouseout = function () {{ btn.style.background = "{VERDE}"; }};
            btn.onclick = function () {{
                window.top.postMessage({{
                    type: "lumen-word-download",
                    fileName: {json.dumps(file_name)},
                    mime: {json.dumps(MIME_DOCX)},
                    b64: {json.dumps(b64)},
                }}, "*");
            }};
        }})();
        </script>
        """,
        height=52,
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
    _instalar_descarga_edge()
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
