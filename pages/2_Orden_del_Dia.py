"""Orden del día, elevación a CS y revisión Secretaría General Académica — prototipo LUMEN."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from data.calendario import (
    ORGANO_DEFAULT_POR_UA,
    ORGANOS_ELEVABLES_A_CS,
    ORGANOS_FECHA_LIBRE,
    fecha_cs_desde_opcion,
    opciones_fecha_cs,
    proxima_fecha_cs,
    reuniones_cs,
)
from data.catalogs import (
    ANIOS,
    ETIQUETAS_ESTADO,
    SEDES,
    UNIDADES_ACADEMICAS,
    UNIDADES_CARGA_CS_DIRECTA,
)
from data.orden_cs import ordenar_temas_consejo_superior
from data.storage import (
    actualizar_tema,
    devolver_tema_a_cd,
    elevar_tema_a_cs,
    eliminar_tema,
    incorporar_tema_cs,
    load_temas,
)
from forms.editar_tema import render_adjunto_en_edicion, render_editar_tema
from services.adjuntos import leer_adjunto, tiene_adjunto
from services.orden_dia import generar_orden_del_dia, nombre_archivo_od
from ui import guardar_word_en_sesion, mostrar_descarga_word, setup_page, sidebar_brand

setup_page("Orden del día · LUMEN")
sidebar_brand("Orden del día")

st.markdown("## Orden del día")
st.caption(
    "Cada unidad descarga su propio Word (CD / CI / CE) para la fecha que acordó. "
    "Todos pueden descargar el orden del día del Consejo Superior por sesión institucional."
)

temas = load_temas()

ESTADOS_CD_OD = {"en_orden_del_dia", "aprobado_cd", "borrador"}
ESTADOS_CS_OD = {"pendiente_revision_sga", "en_orden_del_dia_cs", "elevado_cs", "aprobado_cs"}
ESTADOS_CS_PUBLICO = ESTADOS_CS_OD


def _fmt_estado(estado: str) -> str:
    return ETIQUETAS_ESTADO.get(estado, estado)


def _alerta_devolucion_sga(tema: dict) -> None:
    """Muestra el motivo de devolución de forma visible para la UA."""
    if not tema.get("devuelto_sga_en"):
        return
    obs = str(tema.get("observacion_sga") or "").strip()
    if obs:
        st.error(f"**Motivo de devolución (Secretaría General Académica):** {obs}")
    st.warning(
        "Tema **devuelto por la Secretaría General Académica**. "
        "Podés modificarlo, aprobarlo nuevamente en consejo o eliminarlo."
    )


def _tarjeta_tema(tema: dict) -> None:
    elevacion = ""
    if tema.get("elevado_desde_cd"):
        origen = tema.get("organo_origen", "CD")
        elevacion = f"<br/>Elevado desde {origen} ({tema.get('fecha_cd', '—')})"
    devolucion = ""
    if tema.get("devuelto_sga_en"):
        obs = tema.get("observacion_sga", "")
        devolucion = "<br/><strong>Devuelto por Secretaría General Académica</strong>"
        if obs:
            devolucion += f" — {obs}"
    adjunto_txt = ""
    if tiene_adjunto(tema.get("id", "")) or tema.get("adjunto"):
        nombre = (tema.get("adjunto") or {}).get("nombre_original", "documento adjunto")
        adjunto_txt = f"<br/>📎 Adjunto: {nombre}"
    st.markdown(
        f"""
        <div class="lumen-card">
        <h4>{tema.get('actividad')}</h4>
        <div class="lumen-meta">
        <strong>{tema.get('id')}</strong> · {tema.get('unidad_academica')} · {tema.get('sede')} · {tema.get('anio')}<br/>
        Sesión: {tema.get('organo_tratamiento', '—')} · {tema.get('fecha_reunion', 'Sin fecha')}<br/>
        Estado: {_fmt_estado(tema.get('estado', ''))}{elevacion}{devolucion}{adjunto_txt}<br/>
        PEI: {"Sí — " + tema.get('objetivo_especifico','') if tema.get('impacta_pei') else "No"}
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _boton_descarga_adjunto(tema: dict) -> None:
    tema_id = tema.get("id", "")
    payload = leer_adjunto(tema_id)
    if not payload:
        return
    data, meta = payload
    st.download_button(
        "Descargar adjunto",
        data=data,
        file_name=meta.get("nombre_original", "adjunto"),
        mime=meta.get("mime") or "application/octet-stream",
        key=f"dl_adj_card_{tema_id}",
    )


def _boton_descarga(
    temas_doc: list,
    ua_doc: str,
    sede_doc: str,
    anio_doc: str,
    organo: str,
    fecha_doc: str | None,
    *,
    key: str,
    label: str | None = None,
) -> None:
    """Generar Word y mostrar enlace de descarga (como Consejo de Investigación)."""
    if not temas_doc:
        st.info("No hay temas para generar el documento con los filtros actuales.")
        return

    if st.button("Generar Orden del Día", key=f"gen_{key}"):
        doc_bytes = generar_orden_del_dia(
            temas_doc,
            ua_doc,
            sede_doc,
            anio_doc,
            fecha_reunion=fecha_doc,
            organo=organo,
        )
        fecha_iso = next(
            (t.get("fecha_reunion_iso") for t in temas_doc if t.get("fecha_reunion_iso")),
            None,
        )
        archivo = nombre_archivo_od(organo, ua_doc, anio_doc, fecha_doc, fecha_iso=fecha_iso)
        guardar_word_en_sesion(doc_bytes, archivo, dl_key=key)

    mostrar_descarga_word(key)


def _temas_cs_sesion(anio: str, fecha_legible: str | None = None) -> list[dict]:
    out = [
        t
        for t in temas
        if t.get("anio") == anio
        and t.get("organo_tratamiento") == "Consejo Superior"
        and t.get("estado") in ESTADOS_CS_PUBLICO
    ]
    if fecha_legible:
        out = [t for t in out if t.get("fecha_reunion") == fecha_legible]
    return out


def _organo_sugerido_ua(ua: str) -> str:
    return ORGANO_DEFAULT_POR_UA.get(ua, "Consejo Directivo")


tab_ua, tab_cs, tab_elevar, tab_sga = st.tabs(
    [
        "Mi consejo de unidad",
        "Orden del día — Consejo Superior",
        "Elevar a Consejo Superior",
        "Secretaría General Académica",
    ]
)

# ── Tab 1: OD de la UA (CD / CI / CE) ───────────────────────────────────────
with tab_ua:
    st.markdown("### Descargar el orden del día de tu unidad")
    st.caption(
        "Elegí unidad, órgano y **fecha de sesión** (la misma que cargaste en **Cargar temas**). "
        "Generá el Word para la reunión del Consejo Directivo, de Investigación o de Extensión."
    )

    ua_cd = st.selectbox("Unidad académica *", UNIDADES_ACADEMICAS, key="ua_cd")

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        organos_ua = sorted(ORGANOS_FECHA_LIBRE)
        organo_sug = _organo_sugerido_ua(ua_cd)
        organo_cd = st.selectbox(
            "Órgano *",
            organos_ua,
            index=organos_ua.index(organo_sug) if organo_sug in organos_ua else 0,
            key="organo_cd",
        )
    with c2:
        anio_cd = st.selectbox("Año", ANIOS, index=ANIOS.index("2026"), key="anio_cd")
    with c3:
        sede_cd = st.selectbox("Sede", ["Todas"] + SEDES, key="sede_cd")

    filtro_cd = [
        t
        for t in temas
        if t.get("unidad_academica") == ua_cd
        and t.get("anio") == anio_cd
        and t.get("organo_tratamiento") == organo_cd
        and t.get("estado") in ESTADOS_CD_OD | {"aprobado_cd"}
    ]
    if sede_cd != "Todas":
        filtro_cd = [t for t in filtro_cd if t.get("sede") == sede_cd]

    fechas_cd = sorted({t.get("fecha_reunion") for t in filtro_cd if t.get("fecha_reunion")})
    fecha_cd = st.selectbox(
        "Fecha de sesión *",
        ["— Elegí una fecha —"] + fechas_cd if fechas_cd else ["— Sin fechas cargadas —"],
        key="fecha_cd_sel",
    )

    filtro_fecha = filtro_cd
    if fecha_cd not in {"— Elegí una fecha —", "— Sin fechas cargadas —", "Todas"}:
        filtro_fecha = [t for t in filtro_cd if t.get("fecha_reunion") == fecha_cd]

    st.metric(f"Temas para el OD — {organo_cd}", len(filtro_fecha))

    with st.container(border=True):
        st.markdown("#### Generar y descargar Word del consejo de unidad")
        if fecha_cd in {"— Elegí una fecha —", "— Sin fechas cargadas —"}:
            st.warning(
                "Seleccioná una **fecha de sesión** con temas cargados. "
                "Si no aparece ninguna, cargá temas en **Cargar temas** con esa fecha."
            )
        else:
            _boton_descarga(
                filtro_fecha,
                ua_cd,
                sede_cd if sede_cd != "Todas" else (filtro_fecha[0].get("sede", "—") if filtro_fecha else "—"),
                anio_cd,
                organo_cd,
                fecha_cd,
                key="dl_ua_top",
                label=f"Descargar Word — {organo_cd}",
            )

    if not filtro_fecha:
        st.info(f"No hay temas de **{organo_cd}** para los filtros elegidos.")
    else:
        st.markdown("#### Temas de la sesión")
        edit_id = st.session_state.get("lumen_edit_tema_id")
        for tema in filtro_fecha:
            _tarjeta_tema(tema)
            _alerta_devolucion_sga(tema)
            if tiene_adjunto(tema["id"]):
                _boton_descarga_adjunto(tema)
            b1, b2, b3, b4 = st.columns(4)
            with b1:
                if st.button("Aprobar en consejo", key=f"apr_cd_{tema['id']}"):
                    actualizar_tema(tema["id"], {"estado": "aprobado_cd"})
                    st.rerun()
            with b2:
                if st.button("Modificar", key=f"mod_{tema['id']}"):
                    st.session_state["lumen_edit_tema_id"] = tema["id"]
                    st.rerun()
            with b3:
                if st.button("Marcar borrador", key=f"bor_{tema['id']}"):
                    actualizar_tema(tema["id"], {"estado": "borrador"})
                    st.rerun()
            with b4:
                if st.button("Eliminar", key=f"del_cd_{tema['id']}"):
                    if st.session_state.get("lumen_edit_tema_id") == tema["id"]:
                        st.session_state.pop("lumen_edit_tema_id", None)
                    eliminar_tema(tema["id"])
                    st.rerun()
            if tema.get("estado") == "aprobado_cd":
                st.caption("→ **Elevar a CS** (pestaña *Elevar a Consejo Superior*)")

            if edit_id == tema["id"]:
                accion = render_editar_tema(tema)
                if accion == "saved":
                    st.session_state.pop("lumen_edit_tema_id", None)
                    st.success("Tema actualizado. Revisá y aprobá en consejo si corresponde.")
                    st.rerun()
                if accion == "cancelled":
                    st.session_state.pop("lumen_edit_tema_id", None)
                    st.rerun()
                render_adjunto_en_edicion(tema)

# ── Tab 2: OD Consejo Superior (público, todas las UA) ───────────────────────
with tab_cs:
    st.markdown("### Orden del día del Consejo Superior")
    st.caption(
        "Disponible para **todas las unidades**. Elegí la sesión del cronograma institucional "
        "y descargá el Word consolidado con todos los temas de esa reunión."
    )

    c1, c2 = st.columns(2)
    with c1:
        anio_cs = st.selectbox("Año", ANIOS, index=ANIOS.index("2026"), key="anio_cs_pub")
    with c2:
        calendario_cs = opciones_fecha_cs(anio_cs, "San Juan", incluir_todas=True)
        if not calendario_cs:
            st.warning(f"No hay calendario CS cargado para {anio_cs}.")
            opcion_cs_pub = None
        else:
            proxima = proxima_fecha_cs(anio_cs, "San Juan")
            idx_def = 0
            if proxima:
                et = f"{proxima['fecha_legible']} · {proxima['etiqueta']}"
                if et in calendario_cs:
                    idx_def = calendario_cs.index(et)
            opcion_cs_pub = st.selectbox(
                "Sesión del Consejo Superior *",
                calendario_cs,
                index=idx_def,
                key="opcion_cs_pub",
            )

    reunion_pub = fecha_cs_desde_opcion(opcion_cs_pub, anio_cs) if opcion_cs_pub else None
    fecha_legible_cs = reunion_pub["fecha_legible"] if reunion_pub else None

    temas_cs = _temas_cs_sesion(anio_cs, fecha_legible_cs)
    st.metric("Temas en el OD del Consejo Superior", len(temas_cs))

    with st.container(border=True):
        st.markdown("#### Generar y descargar Word — Consejo Superior")
        if reunion_pub:
            st.write(
                f"**Sesión:** {reunion_pub['fecha_legible']} · "
                f"{reunion_pub.get('etiqueta', '')} · "
                f"{reunion_pub.get('modalidad', '').capitalize()}"
            )
            _boton_descarga(
                temas_cs,
                "Consejo Superior — UCCuyo",
                reunion_pub.get("sede", "Todas"),
                anio_cs,
                "Consejo Superior",
                fecha_legible_cs,
                key="dl_cs_pub",
                label=f"Descargar Word — Consejo Superior — {fecha_legible_cs}",
            )
        else:
            st.warning("Elegí una sesión del cronograma CS.")

    if temas_cs:
        st.markdown("#### Temas incluidos en esta sesión")
        for tema in ordenar_temas_consejo_superior(temas_cs):
            origen = "Elevado desde UA" if tema.get("elevado_desde_cd") else "Carga directa"
            st.caption(f"{origen} · {tema.get('unidad_academica')}")
            _tarjeta_tema(tema)
    elif reunion_pub:
        st.info(
            "Todavía no hay temas cargados para esta sesión del CS. "
            "Podés descargar un Word vacío o aguardar elevaciones desde las unidades."
        )

    with st.expander("Ver cronograma CS del año"):
        rows = [
            {
                "Fecha": r["fecha_legible"],
                "Sede": r.get("sede"),
                "Modalidad": r.get("modalidad"),
                "Temas cargados": len(_temas_cs_sesion(anio_cs, r["fecha_legible"])),
            }
            for r in reuniones_cs(anio_cs)
        ]
        st.dataframe(rows, use_container_width=True, hide_index=True)

# ── Tab 3: Elevación UA → CS ────────────────────────────────────────────────
with tab_elevar:
    st.markdown("### Enviar temas aprobados al Consejo Superior")
    st.caption(
        "Tras el consejo de la unidad (CD, CI o CE), elevá los temas aprobados. "
        "La **Secretaría General Académica** los revisará antes de incorporarlos al orden del día del CS."
    )

    c1, c2 = st.columns(2)
    with c1:
        ua_el = st.selectbox("Unidad académica origen", UNIDADES_ACADEMICAS, key="ua_el")
    with c2:
        anio_el = st.selectbox("Año", ANIOS, index=ANIOS.index("2026"), key="anio_el")

    candidatos = [
        t
        for t in temas
        if t.get("unidad_academica") == ua_el
        and t.get("anio") == anio_el
        and t.get("organo_tratamiento") in ORGANOS_ELEVABLES_A_CS
        and t.get("estado") == "aprobado_cd"
        and not t.get("elevado_desde_cd")
    ]

    st.metric("Temas aprobados listos para elevar", len(candidatos))

    if not candidatos:
        st.info("No hay temas aprobados pendientes de elevación para esta unidad.")
    else:
        sede_el = candidatos[0].get("sede", "San Juan")
        calendario = opciones_fecha_cs(anio_el, sede_el, incluir_todas=True)
        if not calendario:
            st.warning(f"No hay calendario CS para {anio_el}.")
        else:
            proxima = proxima_fecha_cs(anio_el, sede_el)
            idx_def = 0
            if proxima:
                et = f"{proxima['fecha_legible']} · {proxima['etiqueta']}"
                if et in calendario:
                    idx_def = calendario.index(et)

            opcion_cs = st.selectbox(
                "Sesión del Consejo Superior destino *",
                calendario,
                index=idx_def,
                key="opcion_cs_elevar",
            )
            reunion = fecha_cs_desde_opcion(opcion_cs, anio_el)

            for tema in candidatos:
                _tarjeta_tema(tema)
                if st.button(f"Elevar a CS — {tema['actividad'][:40]}", key=f"elv_{tema['id']}"):
                    if reunion:
                        try:
                            elevar_tema_a_cs(tema["id"], reunion)
                            st.success(
                                f"Tema enviado a la Secretaría General Académica para sesión CS del "
                                f"{reunion['fecha_legible']}."
                            )
                            st.rerun()
                        except ValueError as e:
                            st.error(str(e))

# ── Tab 4: Secretaría General Académica ─────────────────────────────────────
with tab_sga:
    st.markdown("### Revisión — Secretaría General Académica")
    st.caption(
        "Espacio de trabajo de la **Secretaría General Académica (SGA)**: incorporar, devolver "
        "o aprobar temas elevados por las UA. "
        "La descarga del Word del CS está en la pestaña **Orden del día — Consejo Superior**."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        anio_sga = st.selectbox("Año", ANIOS, index=ANIOS.index("2026"), key="anio_sga")
    with c2:
        filtro_sga_est = st.selectbox(
            "Estado",
            ["Todos", "Pendiente de revisión", "En orden del día CS", "Aprobado CS"],
            key="est_sga",
        )
    with c3:
        origen_sga = st.selectbox(
            "Origen",
            ["Todos", "Elevados desde UA", "Carga directa CS"],
            key="orig_sga",
        )

    filtro_cs = [
        t
        for t in temas
        if t.get("anio") == anio_sga
        and t.get("organo_tratamiento") == "Consejo Superior"
        and t.get("estado") in ESTADOS_CS_OD
    ]

    map_est = {
        "Pendiente de revisión": "pendiente_revision_sga",
        "En orden del día CS": "en_orden_del_dia_cs",
        "Aprobado CS": "aprobado_cs",
    }
    if filtro_sga_est != "Todos":
        filtro_cs = [t for t in filtro_cs if t.get("estado") == map_est[filtro_sga_est]]
    if origen_sga == "Elevados desde UA":
        filtro_cs = [t for t in filtro_cs if t.get("elevado_desde_cd")]
    elif origen_sga == "Carga directa CS":
        filtro_cs = [t for t in filtro_cs if not t.get("elevado_desde_cd")]

    fechas_cs = sorted({t.get("fecha_reunion") for t in filtro_cs if t.get("fecha_reunion")})
    fecha_cs = st.selectbox(
        "Fecha sesión CS",
        ["Todas"] + fechas_cs if fechas_cs else ["Todas"],
        key="fecha_cs_sga",
    )
    if fecha_cs != "Todas":
        filtro_cs = [t for t in filtro_cs if t.get("fecha_reunion") == fecha_cs]

    pendientes = sum(1 for t in filtro_cs if t.get("estado") == "pendiente_revision_sga")
    st.metric("Temas en revisión", len(filtro_cs), delta=f"{pendientes} pendientes" if pendientes else None)

    if not filtro_cs:
        st.info("No hay temas para revisar con estos filtros.")
    else:
        for tema in filtro_cs:
            _tarjeta_tema(tema)
            origen = "Elevado desde UA" if tema.get("elevado_desde_cd") else "Carga directa"
            st.caption(f"Origen: **{origen}** · Unidad: **{tema.get('unidad_academica')}**")

            b1, b2, b3, b4 = st.columns(4)
            with b1:
                if tema.get("estado") == "pendiente_revision_sga":
                    if st.button("Incorporar al OD CS", key=f"inc_{tema['id']}"):
                        incorporar_tema_cs(tema["id"])
                        st.rerun()
            with b2:
                if tema.get("estado") in {"pendiente_revision_sga", "en_orden_del_dia_cs", "elevado_cs"}:
                    if st.button("Aprobar CS", key=f"apcs_{tema['id']}"):
                        actualizar_tema(tema["id"], {"estado": "aprobado_cs"})
                        st.rerun()
            with b4:
                if st.button("Eliminar", key=f"del_sga_{tema['id']}"):
                    eliminar_tema(tema["id"])
                    st.rerun()

            if tema.get("estado") == "pendiente_revision_sga" and tema.get("elevado_desde_cd"):
                with st.form(f"devolver_{tema['id']}"):
                    st.caption("Devolver a la unidad académica para corrección")
                    obs = st.text_area(
                        "Motivo de devolución *",
                        key=f"obs_{tema['id']}",
                        placeholder="Ej: Falta resolución de CD",
                        height=80,
                    )
                    if st.form_submit_button("Devolver a UA", type="primary"):
                        if not obs.strip():
                            st.error("Indicá el motivo de devolución para que la UA sepa qué corregir.")
                        else:
                            devolver_tema_a_cd(tema["id"], obs)
                            st.rerun()

        with st.expander("Vista tabla"):
            st.dataframe(pd.DataFrame(filtro_cs), use_container_width=True)

st.markdown("---")
with st.expander("Unidades con carga directa al Consejo Superior"):
    st.write("Estas unidades cargan temas directamente al OD del CS (sin pasar por consejo de unidad):")
    for ua in sorted(UNIDADES_CARGA_CS_DIRECTA):
        st.write(f"- {ua}")
