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
    "En este prototipo **LUMEN** podés adjuntar el documento al tema "
    "(PDF, Word, Excel, etc., hasta 10 MB) sin usar un Drive personal. "
    "En Cloud el archivo vive en el servidor de la app (no en tu Google Drive); "
    "puede borrarse si la app se redespliega. La integración con Drive institucional "
    "queda para cuando se active como en Consejo de Investigación."
)

st.info(
    "**Flujo LUMEN (ahorra pasos):** 1) Cargar tema + archivo → 2) Miembros del consejo "
    "descargan, leen y aprueban → 3) **Elevar a Consejo Superior** traslada el tema **y** "
    "el archivo (sin volver a subir) → 4) SGA y CS descargan el mismo documento.\n\n"
    "En Cloud el archivo vive en la sesión/servidor de la app (no en tu Drive); "
    "puede borrarse si la app se redespliega. Drive institucional queda para producción."
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

ua_f = st.selectbox("Unidad académica", ["Todas"] + UNIDADES_ACADEMICAS, key="adj_ua")
c1, c2 = st.columns([3, 1])
with c1:
    anio_f = st.selectbox("Año", ANIOS, index=ANIOS.index("2026"), key="adj_anio")
with c2:
    solo_sin = st.checkbox("Solo sin archivo", value=False, key="adj_sin")

temas = load_temas()
filtrados = [t for t in temas if t.get("anio") == anio_f]
if ua_f != "Todas":
    from data.catalogs import tema_en_unidades

    filtrados = [t for t in filtrados if tema_en_unidades(t, [ua_f])]
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
