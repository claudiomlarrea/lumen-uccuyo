"""Formulario condicional — Consejo de Investigación (campos extendidos)."""

from __future__ import annotations

from typing import Any

import streamlit as st

from data.investigacion import (
    ACTAS_CI_2026,
    CATEGORIAS_INVESTIGADOR,
    MAX_UNIDADES_ACADEMICAS,
    TIPOS_CI,
    TIPOS_FINANCIAMIENTO,
    UNIDADES_CI,
    es_categorizacion,
    requiere_equipo,
    requiere_puntaje,
)


def render_campos_investigacion(*, key: str = "inv", unidad_carga: str = "") -> dict[str, Any]:
    """Muestra campos CI según tipo y devuelve dict crudo para validar/armar bloque."""
    st.markdown("#### Datos Consejo de Investigación")
    st.caption(
        "Mismos campos que el sistema productivo. Se guardan en LUMEN y alimentan "
        "la simulación hacia el sheet de Investigación (y PEI si impacta)."
    )

    tipo_ci = st.selectbox("Tipo de actividad (CI) *", TIPOS_CI, key=f"{key}_tipo_ci")

    c1, c2 = st.columns([3, 1])
    with c1:
        titulo = st.text_input(
            "Denominación del tema *",
            placeholder="Título del proyecto, informe, jornada, etc.",
            key=f"{key}_titulo",
        )
    with c2:
        puntaje_raw = ""
        if requiere_puntaje(tipo_ci):
            puntaje_raw = st.text_input("Puntaje", placeholder="Ej: 87,9", key=f"{key}_puntaje")

    descripcion = st.text_area(
        "Descripción (máx. 50 palabras)",
        key=f"{key}_descripcion",
        height=100,
    )

    raw: dict[str, Any] = {
        "tipo_ci": tipo_ci,
        "titulo": titulo,
        "descripcion": descripcion,
        "puntaje_raw": puntaje_raw,
    }

    if es_categorizacion(tipo_ci):
        c_doc1, c_doc2 = st.columns(2)
        with c_doc1:
            raw["apellido_nombre_docente"] = st.text_input(
                "Apellido y nombre del docente",
                key=f"{key}_nombre_doc",
            )
        with c_doc2:
            raw["dni_docente"] = st.text_input("DNI", key=f"{key}_dni")
    elif requiere_equipo(tipo_ci):
        c_dir1, c_dir2 = st.columns(2)
        with c_dir1:
            raw["director"] = st.text_input("Director", key=f"{key}_director")
        with c_dir2:
            raw["cat_director"] = st.selectbox(
                "Categoría del director",
                CATEGORIAS_INVESTIGADOR,
                key=f"{key}_cat_dir",
            )

        c_cod1, c_cod2 = st.columns(2)
        with c_cod1:
            raw["codirector"] = st.text_input("Codirector", key=f"{key}_codirector")
        with c_cod2:
            raw["cat_codirector"] = st.selectbox(
                "Categoría del codirector",
                CATEGORIAS_INVESTIGADOR,
                key=f"{key}_cat_cod",
            )

        raw["equipo"] = st.text_area(
            "Equipo de investigación (máx. 50 palabras)",
            key=f"{key}_equipo",
            height=80,
        )

        c_eq1, c_eq2, c_eq3 = st.columns(3)
        with c_eq1:
            raw["instituto"] = st.text_input("Instituto de investigación", key=f"{key}_inst")
        with c_eq2:
            raw["catedra"] = st.text_input("Cátedra (si corresponde)", key=f"{key}_catedra")
        with c_eq3:
            raw["alumnos"] = st.text_input("Número de alumnos", key=f"{key}_alumnos")

        c_res1, c_res2 = st.columns(2)
        with c_res1:
            raw["resolucion_cd"] = st.text_input(
                "Resolución CD",
                max_chars=10,
                placeholder="Ej: 665",
                key=f"{key}_res_cd",
            )
        with c_res2:
            raw["resolucion_cs"] = st.text_input(
                "Resolución CS",
                max_chars=10,
                placeholder="Ej: 657",
                key=f"{key}_res_cs",
            )

    st.markdown("**Unidad académica**")
    st.caption(
        f"Máximo {MAX_UNIDADES_ACADEMICAS} unidades. "
        "Indicá a qué UA pertenece el tema (como en el sistema productivo)."
    )
    default_ua: list[str] = []
    if unidad_carga and unidad_carga in UNIDADES_CI and unidad_carga != "Secretaría Investigación":
        default_ua = [unidad_carga]
    raw["unidades_academicas"] = st.multiselect(
        "Unidades académicas del tema *",
        UNIDADES_CI,
        default=default_ua,
        max_selections=MAX_UNIDADES_ACADEMICAS,
        key=f"{key}_unidades",
        label_visibility="collapsed",
    )

    if not es_categorizacion(tipo_ci):
        c_fin1, c_fin2, c_fin3 = st.columns(3)
        with c_fin1:
            raw["tipo_financiamiento"] = st.selectbox(
                "Tipo de financiamiento",
                TIPOS_FINANCIAMIENTO,
                key=f"{key}_tipo_fin",
            )
        with c_fin2:
            raw["fuente_financiamiento"] = st.text_input(
                "Fuente de financiamiento",
                key=f"{key}_fuente_fin",
            )
        with c_fin3:
            raw["monto_financiamiento"] = st.number_input(
                "Monto en pesos (sin puntos)",
                min_value=0,
                step=1000,
                value=None,
                key=f"{key}_monto",
            )

    opciones_acta = ["— Sin acta —"] + [
        f"Acta {n} — {fecha}" for n, fecha in sorted(ACTAS_CI_2026.items())
    ]
    acta_sel = st.selectbox("Orden del día / Acta CI (opcional)", opciones_acta, key=f"{key}_acta")
    if acta_sel != "— Sin acta —":
        numero = int(acta_sel.split("—")[0].replace("Acta", "").strip())
        raw["numero_acta"] = numero
        raw["fecha_acta"] = ACTAS_CI_2026.get(numero, "")

    raw["responsable_de_carga"] = st.text_input(
        "Responsable de carga",
        placeholder="Correo o nombre de quien carga",
        key=f"{key}_responsable",
    )

    return raw
