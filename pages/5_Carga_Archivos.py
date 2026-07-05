"""Carga de archivos adjuntos — patrón Consejo de Investigación (prototipo local)."""

from __future__ import annotations

import streamlit as st

from data.catalogs import ANIOS, UNIDADES_ACADEMICAS
from data.investigacion import ACTAS_CI_2026
from data.storage import load_temas
from forms.adjunto import render_gestion_adjunto_tema
from services.adjuntos import tiene_adjunto
from ui import setup_page, sidebar_brand

setup_page("Carga de archivos · LUMEN")
sidebar_brand("Carga de archivos")

st.markdown("## Carga de archivos")
st.caption(
    "En el sistema productivo de **Consejo de Investigación**, tras guardar el tema en la planilla "
    "se sube el documento a **Google Drive** (carpeta del acta → subcarpeta de la unidad académica). "
    "En este prototipo LUMEN el archivo se guarda **localmente** vinculado al id del tema."
)

st.info(
    "**Flujo CI productivo:** 1) Cargar tema → 2) Abrir carpeta del acta en Drive → "
    "3) Entrar a la carpeta de la UA → 4) Subir archivo.\n\n"
    "**Flujo LUMEN (prototipo):** 1) Cargar tema → 2) Subir archivo acá (opcional, ahora o después)."
)

st.markdown("### Referencia — carpetas Drive Consejo de Investigación (2026)")
with st.expander("Ver actas CI y enlace al flujo Drive (solo referencia)"):
    st.caption(
        "Estas actas son las del formulario CI. En producción, cada acta tiene una carpeta Drive "
        "con subcarpetas por unidad académica."
    )
    for numero, fecha in sorted(ACTAS_CI_2026.items()):
        st.write(f"- **Acta {numero}** — {fecha}")

st.markdown("### Adjuntar documento a un tema cargado")

c1, c2, c3 = st.columns(3)
with c1:
    ua_f = st.selectbox("Unidad académica", ["Todas"] + UNIDADES_ACADEMICAS, key="adj_ua")
with c2:
    anio_f = st.selectbox("Año", ANIOS, index=ANIOS.index("2026"), key="adj_anio")
with c3:
    solo_sin = st.checkbox("Solo temas sin archivo", value=False, key="adj_sin")

temas = load_temas()
filtrados = [t for t in temas if t.get("anio") == anio_f]
if ua_f != "Todas":
    filtrados = [t for t in filtrados if t.get("unidad_academica") == ua_f]
if solo_sin:
    filtrados = [t for t in filtrados if not tiene_adjunto(t["id"])]

st.metric("Temas", len(filtrados))

if not filtrados:
    st.warning("No hay temas para los filtros elegidos. Cargá temas en **Cargar temas** primero.")
else:
    opciones = {
        f"{t.get('actividad', '(sin título)')[:50]} — {t['id']}": t for t in filtrados
    }
    sel = st.selectbox("Elegir tema *", list(opciones.keys()), key="adj_tema_sel")
    tema = opciones[sel]

    with st.container(border=True):
        render_gestion_adjunto_tema(tema)

    st.markdown("---")
    st.markdown("#### Otros temas del filtro")
    for t in filtrados:
        if t["id"] == tema["id"]:
            continue
        flag = "📎" if tiene_adjunto(t["id"]) else "—"
        st.caption(f"{flag} {t.get('actividad')} · {t['id']}")
