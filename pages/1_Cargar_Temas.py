"""Carga de temas — registro canónico LUMEN (prototipo local)."""

from __future__ import annotations

import streamlit as st

from data.calendario import (
    ORGANOS_TRATAMIENTO,
    fecha_cs_desde_opcion,
    formato_fecha,
    opciones_fecha_cs,
    organo_default_index,
    proxima_fecha_cs,
    usa_calendario_cs,
)
from data.catalogs import (
    ACTIVIDADES_EJEMPLO,
    AMBITOS,
    ANIOS,
    ETIQUETAS_ESTADO,
    SEDES,
    TIPOS_ACTIVIDAD,
    UNIDADES_ACADEMICAS,
    all_objetivos,
    objetivo_general_de,
    puede_cargar_cs_directo,
    sugerir_objetivo,
)
from data.investigacion import armar_bloque_investigacion, validar_campos_investigacion
from data.storage import agregar_tema
from forms.adjunto import procesar_adjunto_al_guardar, render_uploader_adjunto
from ui import setup_page, sidebar_brand
from forms.investigacion import render_campos_investigacion

setup_page("Cargar temas · LUMEN")
sidebar_brand("Cargar temas")

st.markdown("## Cargar temas")
st.caption("Registro único para orden del día, PEI e Investigación. Los datos quedan solo en este prototipo.")

st.info("Los datos se guardan solo en este prototipo (archivo local). No se envían a Google Sheets productivos.")

st.subheader("Identificación")
c1, c2, c3 = st.columns(3)
with c1:
    ua = st.selectbox("Unidad académica / administrativa *", UNIDADES_ACADEMICAS, key="ua")
with c2:
    sede = st.selectbox("Sede *", SEDES, key="sede")
with c3:
    anio = st.selectbox("Año *", ANIOS, index=ANIOS.index("2026"), key="anio")

c4, c5 = st.columns(2)
with c4:
    idx_ambito = AMBITOS.index("Investigación") if ua == "Secretaría Investigación" else 0
    ambito = st.selectbox("Ámbito *", AMBITOS, index=idx_ambito, key="ambito")
with c5:
    if ua == "Secretaría Investigación":
        st.session_state["es_investigacion"] = "Sí"
        st.selectbox(
            "¿Es tema de investigación? *",
            ["Sí"],
            index=0,
            disabled=True,
            key="es_investigacion",
            help="La Secretaría Investigación usa siempre el formulario del Consejo de Investigación.",
        )
        es_inv = True
    else:
        es_investigacion = st.selectbox(
            "¿Es tema de investigación? *",
            ["No", "Sí"],
            index=0,
            key="es_investigacion",
        )
        es_inv = es_investigacion == "Sí"

bloque_inv_raw: dict | None = None
tipo = ""
actividad = ""
detalle = ""

if es_inv:
    bloque_inv_raw = render_campos_investigacion(key="carga", unidad_carga=ua)
    tipo = bloque_inv_raw["tipo_ci"]
    actividad = bloque_inv_raw.get("titulo", "")
    detalle = bloque_inv_raw.get("descripcion", "")
else:
    st.subheader("Actividad")
    c6, c7 = st.columns(2)
    with c6:
        tipo = st.selectbox("Tipo de actividad *", TIPOS_ACTIVIDAD, key="tipo")
    with c7:
        actividades_ua = ACTIVIDADES_EJEMPLO.get(ua, [])
        opciones_act = actividades_ua + ["Otra actividad (cargar a mano)"]
        actividad_sel = st.selectbox("Actividad *", opciones_act, key="actividad_sel")

    if actividad_sel == "Otra actividad (cargar a mano)":
        actividad = st.text_input(
            "Escribir actividad (máx. 20 palabras) *",
            placeholder="Describí la actividad en no más de 20 palabras",
            key="actividad_manual",
        )
    else:
        actividad = actividad_sel

    detalle = st.text_input("Detalle (opcional, máx. 20 palabras)", key="detalle")

st.subheader("Sesión del orden del día")
carga_cs_directa = puede_cargar_cs_directo(ua)
if carga_cs_directa:
    st.success(
        f"**{ua}** puede cargar temas **directamente al orden del día del Consejo Superior**."
    )
else:
    st.caption(
        "Flujo habitual: Consejo Directivo de la UA → aprobación → elevación al CS → revisión SGA."
    )

if es_inv:
    organos = ORGANOS_TRATAMIENTO
    idx_org = organos.index("Consejo de Investigación") if "Consejo de Investigación" in organos else 0
    organo = st.selectbox(
        "Órgano de tratamiento *",
        organos,
        index=idx_org,
        key="organo",
        help="Temas de investigación van al Consejo de Investigación de la UA.",
    )
else:
    organo_default = organo_default_index(ua, carga_cs_directa)
    organo = st.selectbox(
        "Órgano de tratamiento *",
        ORGANOS_TRATAMIENTO,
        index=organo_default,
        key="organo",
        help="CD / CI / CE: fecha libre de la unidad. CS: cronograma institucional anual.",
    )

fecha_reunion = ""
fecha_reunion_iso = ""
cs_sede_reunion = ""
cs_modalidad = ""

if usa_calendario_cs(organo):
    calendario = opciones_fecha_cs(str(anio), sede)
    if not calendario:
        st.warning(f"No hay calendario de Consejo Superior para **{anio}**.")
    else:
        incluir_todas = st.checkbox(
            "Mostrar todas las sesiones de CS del año",
            value=False,
            key="cs_ver_todas",
        )
        if incluir_todas:
            calendario = opciones_fecha_cs(str(anio), sede, incluir_todas=True)
        proxima = proxima_fecha_cs(str(anio), sede)
        idx_default = 0
        if proxima:
            et = f"{proxima['fecha_legible']} · {proxima['etiqueta']}"
            if et in calendario:
                idx_default = calendario.index(et)
        opcion_cs = st.selectbox("Fecha del Consejo Superior *", calendario, index=idx_default, key="fecha_cs")
        reunion = fecha_cs_desde_opcion(opcion_cs, str(anio))
        if reunion:
            fecha_reunion = reunion["fecha_legible"]
            fecha_reunion_iso = reunion["fecha_iso"]
            cs_sede_reunion = reunion.get("sede", "")
            cs_modalidad = reunion.get("modalidad", "")
else:
    if es_inv and bloque_inv_raw and bloque_inv_raw.get("fecha_acta"):
        fecha_reunion = bloque_inv_raw["fecha_acta"]
        st.caption(f"Fecha de sesión CI (desde acta): **{fecha_reunion}**")
    else:
        st.caption(f"Indicá la fecha acordada para **{organo}**.")
        fecha_libre = st.date_input(
            f"Fecha del {organo} *",
            value=None,
            format="DD/MM/YYYY",
            key="fecha_organo_libre",
        )
        if fecha_libre:
            fecha_reunion_iso = fecha_libre.isoformat()
            fecha_reunion = formato_fecha(fecha_libre)

if es_inv and bloque_inv_raw and bloque_inv_raw.get("fecha_acta") and not fecha_reunion_iso:
    # Acta CI seleccionada: guardar fecha legible aunque no haya ISO estricto
    pass

st.subheader("Vinculación PEI")
impacta_default = 0 if es_inv else 0
c8, c9 = st.columns(2)
with c8:
    impacta_pei = st.selectbox("¿Impacta PEI? *", ["Sí", "No"], index=impacta_default, key="impacta_pei")
with c9:
    requiere_cs_default = 1 if usa_calendario_cs(organo) else 0
    requiere_cs = st.selectbox(
        "¿Requiere Consejo Superior?",
        ["No", "Sí"],
        index=requiere_cs_default,
        key="requiere_cs",
    )

objetivo = ""
objetivo_sugerido = ""
if impacta_pei == "Sí":
    objetivo_sugerido = sugerir_objetivo(tipo if not es_inv else "Proyecto de investigación")
    todos_objetivos = all_objetivos()
    if objetivo_sugerido:
        st.info(f"Objetivo PEI sugerido: **{objetivo_sugerido}**")
    usar_sugerido = st.checkbox(
        "Usar objetivo sugerido",
        value=bool(objetivo_sugerido),
        disabled=not objetivo_sugerido,
        key="usar_sugerido",
    )
    if usar_sugerido and objetivo_sugerido:
        objetivo = objetivo_sugerido
    else:
        idx_def = 0
        if objetivo_sugerido and objetivo_sugerido in todos_objetivos:
            idx_def = todos_objetivos.index(objetivo_sugerido)
        objetivo = st.selectbox(
            "Objetivo específico PEI *",
            todos_objetivos,
            index=idx_def,
            key="objetivo_manual",
        )

st.subheader("Estado inicial")
if usa_calendario_cs(organo):
    estados_iniciales = ["borrador", "en_orden_del_dia_cs", "pendiente_revision_sga"]
    estado_default = "en_orden_del_dia_cs"
else:
    estados_iniciales = ["borrador", "en_orden_del_dia"]
    estado_default = "en_orden_del_dia"

estado = st.selectbox(
    "Estado *",
    estados_iniciales,
    format_func=lambda x: ETIQUETAS_ESTADO.get(x, x),
    index=estados_iniciales.index(estado_default),
    key="estado",
)

archivo_adjunto = render_uploader_adjunto(key="carga")

if st.button("Guardar tema en LUMEN", type="primary"):
    errores = []
    if not actividad or not str(actividad).strip():
        errores.append("Completá la actividad / denominación.")
    if not es_inv and len(str(actividad).split()) > 20:
        errores.append("La actividad no puede superar 20 palabras.")
    if not es_inv and detalle and len(detalle.split()) > 20:
        errores.append("El detalle no puede superar 20 palabras.")
    if impacta_pei == "Sí" and not objetivo:
        errores.append("Seleccioná un objetivo PEI.")
    if not fecha_reunion and not fecha_reunion_iso:
        errores.append("Indicá la fecha de la sesión del orden del día.")

    investigacion: dict = {}
    if es_inv and bloque_inv_raw:
        errores.extend(validar_campos_investigacion(bloque_inv_raw["tipo_ci"], bloque_inv_raw))
        investigacion = armar_bloque_investigacion(bloque_inv_raw["tipo_ci"], bloque_inv_raw)
        if bloque_inv_raw.get("fecha_acta") and not fecha_reunion:
            fecha_reunion = bloque_inv_raw["fecha_acta"]

    if errores:
        for e in errores:
            st.error(e)
    else:
        record = {
            "unidad_academica": ua,
            "sede": sede,
            "anio": str(anio),
            "ambito": ambito,
            "es_investigacion": es_inv,
            "tipo_actividad": tipo,
            "tipo_manual": "",
            "actividad": str(actividad).strip(),
            "actividad_manual": False,
            "detalle": str(detalle).strip(),
            "organo_tratamiento": organo,
            "fecha_reunion": fecha_reunion,
            "fecha_reunion_iso": fecha_reunion_iso,
            "cs_sede_reunion": cs_sede_reunion,
            "cs_modalidad": cs_modalidad,
            "impacta_pei": impacta_pei == "Sí",
            "requiere_cs": requiere_cs,
            "objetivo_especifico": objetivo if impacta_pei == "Sí" else "",
            "objetivo_general": objetivo_general_de(objetivo) if impacta_pei == "Sí" else "",
            "objetivo_sugerido": objetivo_sugerido if impacta_pei == "Sí" else "",
            "estado": estado,
            "carga_cs_directa": carga_cs_directa and usa_calendario_cs(organo),
            "elevado_desde_cd": False,
            "correo_responsable": investigacion.get("responsable_de_carga", ""),
        }
        if investigacion:
            record["investigacion"] = investigacion
        guardado = agregar_tema(record)
        if procesar_adjunto_al_guardar(guardado["id"], archivo_adjunto):
            st.success(
                f"Tema `{guardado['id']}` registrado **con documento adjunto**. "
                "Ver Orden del día o Impacto en tableros PEI/CI."
            )
        else:
            st.success(f"Tema registrado en LUMEN (id `{guardado['id']}`). Ver Orden del día o Impacto en tableros PEI/CI.")
            if archivo_adjunto is None:
                st.info(
                    "Podés cargar el documento después en **Carga de archivos** "
                    "(mismo flujo que Consejo de Investigación: tema primero, archivo después)."
                )
                if st.button("Ir a Carga de archivos", key="ir_carga_archivos"):
                    st.switch_page("pages/5_Carga_Archivos.py")
