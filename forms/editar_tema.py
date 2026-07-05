"""Formulario de edición de temas por la unidad académica."""

from __future__ import annotations

from typing import Any, Literal, Optional

import streamlit as st

from data.catalogs import AMBITOS, TIPOS_ACTIVIDAD, all_objetivos, objetivo_general_de, sugerir_objetivo
from data.investigacion import armar_bloque_investigacion, validar_campos_investigacion
from data.storage import modificar_tema_unidad
from forms.adjunto import render_gestion_adjunto_tema
from forms.investigacion import prefill_campos_investigacion, render_campos_investigacion

EditAccion = Optional[Literal["saved", "cancelled"]]


def _prefill_generico(tema: dict[str, Any], key: str) -> None:
    flag = f"{key}_prefilled"
    if st.session_state.get(flag):
        return
    tipo = tema.get("tipo_actividad", TIPOS_ACTIVIDAD[0])
    if tipo not in TIPOS_ACTIVIDAD:
        tipo = TIPOS_ACTIVIDAD[0]
    ambito = tema.get("ambito", AMBITOS[0])
    if ambito not in AMBITOS:
        ambito = AMBITOS[0]
    defaults = {
        f"{key}_tipo": tipo,
        f"{key}_actividad": tema.get("actividad", ""),
        f"{key}_detalle": tema.get("detalle", ""),
        f"{key}_ambito": ambito,
        f"{key}_impacta_pei": "Sí" if tema.get("impacta_pei") else "No",
    }
    objetivo = tema.get("objetivo_especifico", "")
    todos = all_objetivos()
    if objetivo and objetivo in todos:
        defaults[f"{key}_objetivo"] = objetivo
    for k, v in defaults.items():
        st.session_state[k] = v
    st.session_state[flag] = True


def _limpiar_prefill(tema_id: str, es_inv: bool) -> None:
    st.session_state.pop(f"edit_{tema_id}_prefilled", None)
    if es_inv:
        st.session_state.pop(f"edit_inv_{tema_id}_prefilled", None)


def render_editar_tema(tema: dict[str, Any]) -> EditAccion:
    """
    Muestra formulario de edición inline.
    Devuelve 'saved', 'cancelled' o None.
    """
    tema_id = tema["id"]
    key = f"edit_{tema_id}"
    inv_key = f"edit_inv_{tema_id}"
    es_inv = bool(tema.get("es_investigacion"))

    st.markdown("#### Modificar tema")
    if tema.get("observacion_sga"):
        st.warning(f"**Observación de la SGA:** {tema['observacion_sga']}")
    elif tema.get("devuelto_sga_en"):
        st.info(
            "Este tema fue devuelto por la Secretaría General Académica. "
            "Guardá los cambios y volvé a **Aprobar en consejo**."
        )

    bloque_inv_raw: dict[str, Any] | None = None
    tipo = ""
    actividad = ""
    detalle = ""
    ambito = tema.get("ambito", AMBITOS[0])
    impacta_pei = "No"
    objetivo = ""

    with st.form(f"form_edit_{tema_id}"):
        if es_inv:
            prefill_campos_investigacion(key=inv_key, inv=tema.get("investigacion") or {}, tema=tema)
            bloque_inv_raw = render_campos_investigacion(
                key=inv_key,
                unidad_carga=str(tema.get("unidad_academica") or ""),
            )
            tipo = bloque_inv_raw["tipo_ci"]
            actividad = bloque_inv_raw.get("titulo", "")
            detalle = bloque_inv_raw.get("descripcion", "")
        else:
            _prefill_generico(tema, key)
            c1, c2 = st.columns(2)
            with c1:
                tipo = st.selectbox("Tipo de actividad *", TIPOS_ACTIVIDAD, key=f"{key}_tipo")
            with c2:
                ambito = st.selectbox("Ámbito *", AMBITOS, key=f"{key}_ambito")
            actividad = st.text_input("Actividad / denominación *", key=f"{key}_actividad")
            detalle = st.text_input("Detalle (opcional, máx. 20 palabras)", key=f"{key}_detalle")
            impacta_pei = st.selectbox("¿Impacta PEI? *", ["Sí", "No"], key=f"{key}_impacta_pei")
            if impacta_pei == "Sí":
                todos_objetivos = all_objetivos()
                idx_def = 0
                prev = tema.get("objetivo_especifico", "")
                sugerido = sugerir_objetivo(tipo)
                if prev and prev in todos_objetivos:
                    idx_def = todos_objetivos.index(prev)
                elif sugerido and sugerido in todos_objetivos:
                    idx_def = todos_objetivos.index(sugerido)
                objetivo = st.selectbox(
                    "Objetivo específico PEI *",
                    todos_objetivos,
                    index=idx_def,
                    key=f"{key}_objetivo",
                )

        c_ok, c_cancel = st.columns(2)
        with c_ok:
            guardar = st.form_submit_button("Guardar cambios", type="primary")
        with c_cancel:
            cancelar = st.form_submit_button("Cancelar")

    if cancelar:
        _limpiar_prefill(tema_id, es_inv)
        return "cancelled"

    if not guardar:
        return None

    errores: list[str] = []
    if not actividad or not str(actividad).strip():
        errores.append("Completá la actividad / denominación.")
    if not es_inv and len(str(actividad).split()) > 20:
        errores.append("La actividad no puede superar 20 palabras.")
    if not es_inv and detalle and len(str(detalle).split()) > 20:
        errores.append("El detalle no puede superar 20 palabras.")

    cambios: dict[str, Any] = {
        "tipo_actividad": tipo,
        "actividad": str(actividad).strip(),
        "detalle": str(detalle).strip(),
    }

    if es_inv and bloque_inv_raw:
        errores.extend(validar_campos_investigacion(bloque_inv_raw["tipo_ci"], bloque_inv_raw))
        investigacion = armar_bloque_investigacion(bloque_inv_raw["tipo_ci"], bloque_inv_raw)
        cambios["investigacion"] = investigacion
        cambios["correo_responsable"] = investigacion.get("responsable_de_carga", "")
    elif not es_inv:
        cambios["ambito"] = ambito
        cambios["impacta_pei"] = impacta_pei == "Sí"
        if impacta_pei == "Sí":
            if not objetivo:
                errores.append("Seleccioná un objetivo PEI.")
            cambios["objetivo_especifico"] = objetivo
            cambios["objetivo_general"] = objetivo_general_de(objetivo)
            cambios["objetivo_sugerido"] = sugerir_objetivo(tipo) or ""
        else:
            cambios["objetivo_especifico"] = ""
            cambios["objetivo_general"] = ""
            cambios["objetivo_sugerido"] = ""

    if errores:
        for err in errores:
            st.error(err)
        return None

    modificar_tema_unidad(tema_id, cambios)
    _limpiar_prefill(tema_id, es_inv)
    return "saved"


def render_adjunto_en_edicion(tema: dict[str, Any]) -> None:
    """Gestión de adjunto fuera del form (opcional, como en CI)."""
    st.markdown("---")
    st.subheader("Documento adjunto")
    render_gestion_adjunto_tema(tema)
