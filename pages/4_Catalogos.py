"""Consulta de catálogos y opciones cargadas a mano."""

import streamlit as st

from data.calendario import load_calendario_cs, reuniones_cs
from data.catalogs import (
    ACTIVIDADES_EJEMPLO,
    TIPOS_ACTIVIDAD,
    TIPO_A_OBJETIVO,
    UNIDADES_ACADEMICAS,
)
from data.storage import load_catalogo_manual, load_temas
from ui import setup_page, sidebar_brand

setup_page("Catálogos · LUMEN")
sidebar_brand("Catálogos")

st.markdown("## Catálogos del prototipo")
st.caption("Desplegables base + opciones incorporadas por carga manual.")

cat = load_catalogo_manual()
temas = load_temas()

t1, t2, t3, t4 = st.tabs(["Unidades académicas", "Tipos de actividad", "Actividades por UA", "Calendario CS"])

with t1:
    st.write(f"**{len(UNIDADES_ACADEMICAS)}** unidades (mismo criterio institucional del PEI / Investigación).")
    st.dataframe({"Unidad académica": UNIDADES_ACADEMICAS}, use_container_width=True)

with t2:
    st.markdown("### Tipos base")
    st.dataframe({"Tipo": TIPOS_ACTIVIDAD}, use_container_width=True)
    st.markdown("### Tipos cargados a mano en este prototipo")
    if cat.get("tipos"):
        st.dataframe({"Tipo manual": cat["tipos"]}, use_container_width=True)
    else:
        st.info("Todavía no se cargaron tipos manuales.")

    st.markdown("### Matriz tipo → objetivo PEI sugerido")
    st.dataframe(
        {
            "Tipo de actividad": list(TIPO_A_OBJETIVO.keys()),
            "Objetivo PEI sugerido": list(TIPO_A_OBJETIVO.values()),
        },
        use_container_width=True,
    )

with t3:
    ua = st.selectbox("Unidad académica", UNIDADES_ACADEMICAS)
    semilla = ACTIVIDADES_EJEMPLO.get(ua, [])
    manuales = cat.get("actividades_por_ua", {}).get(ua, [])
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Semilla del prototipo**")
        if semilla:
            for a in semilla:
                st.write(f"- {a}")
        else:
            st.caption("Sin semilla para esta UA.")
    with c2:
        st.markdown("**Cargadas a mano**")
        if manuales:
            for a in manuales:
                st.write(f"- {a}")
        else:
            st.caption("Sin actividades manuales aún.")

with t4:
    st.markdown("### Consejo Superior — fechas institucionales")
    st.caption(
        "Tomadas del **Cronograma Consejo Superior 2026.pdf**. "
        "Al cargar temas para CS o elevar desde la UA, el usuario elige de esta lista "
        "(igual que las fechas fijas de actas en Consejo de Investigación)."
    )
    anio_cal = st.selectbox("Año del calendario", ["2026", "2027"], key="anio_cal_cs")
    data = load_calendario_cs(anio_cal)
    if not data:
        st.warning(f"Todavía no hay calendario CS cargado para {anio_cal}.")
    else:
        st.write(f"Fuente: **{data.get('fuente', '—')}**")
        rows = []
        for r in reuniones_cs(anio_cal):
            rows.append(
                {
                    "Fecha": r["fecha_legible"],
                    "Sede": r.get("sede"),
                    "Modalidad": r.get("modalidad"),
                    "Etiqueta": r.get("etiqueta"),
                }
            )
        st.dataframe(rows, use_container_width=True, hide_index=True)
        st.info(
            "**Consejos Directivos:** no usan este calendario. "
            "Cada unidad indica la fecha libremente al cargar el tema."
        )

st.markdown("---")
st.markdown("### Resumen de uso en el prototipo")
st.write(f"Temas guardados: **{len(temas)}**")
if temas:
    uas = sorted({t.get("unidad_academica") for t in temas})
    st.write("UA con temas:", ", ".join(uas))
