"""Simulación de impacto PEI e Investigación — sin escribir en Sheets productivos."""

import pandas as pd
import streamlit as st

from data.storage import actualizar_tema, load_temas
from ui import setup_page, sidebar_brand

setup_page("Simulación PEI · LUMEN")
sidebar_brand("Simulación PEI")

st.markdown("## Simulación de publicación")
st.markdown(
    """
    <div class="lumen-note">
    <strong>Importante:</strong> esta pantalla solo simula el impacto en el Tablero PEI y en el sheet
    de Investigación. <em>No escribe</em> en Google Sheets ni en el Formulario Único productivo.
    </div>
    """,
    unsafe_allow_html=True,
)

temas = load_temas()

# Publicables: aprobados CD o CS, impactan PEI
publicables_pei = [
    t
    for t in temas
    if t.get("impacta_pei")
    and t.get("estado") in {"aprobado_cd", "aprobado_cs", "publicado_simulado"}
]
publicables_inv = [
    t
    for t in temas
    if t.get("es_investigacion")
    and t.get("estado") in {"aprobado_cd", "aprobado_cs", "publicado_simulado", "en_orden_del_dia"}
]

c1, c2, c3 = st.columns(3)
c1.metric("Temas totales en LUMEN", len(temas))
c2.metric("Simularían impacto PEI", len(publicables_pei))
c3.metric("Simularían impacto Investigación", len(publicables_inv))

st.markdown("### Publicar simulación")
if st.button("Marcar publicables como 'publicado_simulado'", use_container_width=True):
    n = 0
    for t in publicables_pei:
        actualizar_tema(
            t["id"],
            {
                "estado": "publicado_simulado",
                "publicado_pei_simulado": True,
                "publicado_investigacion_simulado": bool(t.get("es_investigacion")),
            },
        )
        n += 1
    for t in publicables_inv:
        if not t.get("impacta_pei"):
            actualizar_tema(
                t["id"],
                {
                    "publicado_investigacion_simulado": True,
                },
            )
    st.success(f"Simulación actualizada ({n} temas PEI).")
    st.rerun()

st.markdown("### Vista previa — filas que irían al PEI")
if publicables_pei:
    filas_pei = []
    for t in publicables_pei:
        filas_pei.append(
            {
                "ID LUMEN": t.get("id"),
                "Correo (simulado)": "prototipo.lumen@uccuyo.edu.ar",
                "Objetivo específico": t.get("objetivo_especifico"),
                "Actividad": t.get("actividad"),
                "Detalle": t.get("detalle", ""),
                "Resultados": "",
                "AÑO": t.get("anio"),
                "Unidad Académica": t.get("unidad_academica"),
                "Estado": t.get("estado"),
            }
        )
    df_pei = pd.DataFrame(filas_pei)
    st.dataframe(df_pei, use_container_width=True)
    st.download_button(
        "Descargar CSV de simulación PEI",
        data=df_pei.to_csv(index=False).encode("utf-8-sig"),
        file_name="LUMEN_simulacion_PEI.csv",
        mime="text/csv",
    )

    st.markdown("#### Conteos por objetivo PEI")
    st.bar_chart(df_pei["Objetivo específico"].value_counts())
else:
    st.info(
        "No hay temas aprobados con impacto PEI. "
        "En **Orden del día**, aprobá temas (Aprobar CD / Aprobar CS)."
    )

st.markdown("### Vista previa — filas que irían al sheet de Investigación")
if publicables_inv:
    filas_inv = []
    for t in publicables_inv:
        filas_inv.append(
            {
                "ID LUMEN": t.get("id"),
                "AÑO": t.get("anio"),
                "TIPO": t.get("tipo_actividad"),
                "TITULO": t.get("actividad"),
                "DESCRIPCIÓN": t.get("detalle", ""),
                "UNIDAD ACADÉMICA": t.get("unidad_academica"),
                "Estado": t.get("estado"),
            }
        )
    df_inv = pd.DataFrame(filas_inv)
    st.dataframe(df_inv, use_container_width=True)
    st.download_button(
        "Descargar CSV de simulación Investigación",
        data=df_inv.to_csv(index=False).encode("utf-8-sig"),
        file_name="LUMEN_simulacion_Investigacion.csv",
        mime="text/csv",
    )
else:
    st.info("No hay temas de investigación para simular.")
