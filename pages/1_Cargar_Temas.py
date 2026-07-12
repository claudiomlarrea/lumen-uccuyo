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

# Claves del tema a limpiar (NO tocar ua, sede, anio, organo, fecha — carga en lote).
_KEYS_TEMA = (
    "tipo",
    "actividad_sel",
    "actividad_manual",
    "detalle",
    "impacta_pei",
    "requiere_cs",
    "usar_sugerido",
    "objetivo_manual",
    "estado",
)
_INV_SUFFIXES = (
    "tipo_ci",
    "titulo",
    "puntaje",
    "descripcion",
    "nombre_doc",
    "dni",
    "director",
    "cat_dir",
    "codirector",
    "cat_cod",
    "equipo",
    "inst",
    "catedra",
    "alumnos",
    "res_cd",
    "res_cs",
    "unidades",
    "tipo_fin",
    "fuente_fin",
    "monto",
    "acta",
    "responsable",
)


def _limpiar_campos_tema(*, dismiss_success: bool = False) -> None:
    """Debe ejecutarse ANTES de crear widgets (callback o flag al inicio)."""
    for k in _KEYS_TEMA:
        st.session_state.pop(k, None)
    for suf in _INV_SUFFIXES:
        st.session_state.pop(f"carga_{suf}", None)
    nonce = int(st.session_state.get("lumen_carga_nonce", 0))
    st.session_state.pop(f"carga_{nonce}_file", None)
    st.session_state["lumen_carga_nonce"] = nonce + 1
    if dismiss_success:
        st.session_state.pop("lumen_ultimo_tema_guardado", None)


def _on_cargar_otro_tema() -> None:
    _limpiar_campos_tema(dismiss_success=True)


setup_page("Cargar temas · LUMEN")
sidebar_brand("Cargar temas")

# Limpiar DESPUÉS de guardar, antes de dibujar el formulario (evita error de Streamlit).
if st.session_state.pop("lumen_pendiente_limpiar_tema", False):
    _limpiar_campos_tema(dismiss_success=False)

# Limpiar valor legacy del selectbox de catálogo (ya eliminado)
st.session_state.pop("actividad_sel", None)

st.markdown("## Cargar temas")
st.caption("Registro único para orden del día, PEI e Investigación. Los datos quedan solo en este prototipo.")

st.info(
    "Los datos se guardan en este prototipo durante la sesión. "
    "En Streamlit Cloud un redespliegue reinicia el disco: los temas de demo del repositorio "
    "permanecen; los cargados en la app se conservan al cambiar de página, pero pueden "
    "perderse si la app se reinicia. No se envían a Google Sheets productivos."
)

# Errores de validación del intento anterior (arriba, bien visibles)
_errores_prev = st.session_state.pop("lumen_errores_carga", None)
if _errores_prev:
    for e in _errores_prev:
        st.error(e)

st.subheader("Identificación")
# Consejo Directivo / carga habitual: una sola UA.
# Varias UA solo en el formulario de Investigación (como en CI productivo).
ua = st.selectbox(
    "Unidad académica / administrativa *",
    UNIDADES_ACADEMICAS,
    key="ua",
)
ua_principal = ua

c2, c3 = st.columns([3, 1])
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
actividad_sel = ""

if es_inv:
    bloque_inv_raw = render_campos_investigacion(key="carga", unidad_carga=ua_principal)
    tipo = bloque_inv_raw["tipo_ci"]
    actividad = bloque_inv_raw.get("titulo", "")
    detalle = bloque_inv_raw.get("descripcion", "")
else:
    st.subheader("Actividad")
    tipo = st.selectbox("Tipo de actividad *", TIPOS_ACTIVIDAD, key="tipo")
    actividad_sel = ""
    actividad = st.text_input(
        "Denominación del tema / actividad *",
        placeholder="Ej: Convenio con municipalidad de Vicuña",
        key="actividad_manual",
        help="Nombre corto del tema (máx. 20 palabras).",
    )
    detalle = st.text_input(
        "Detalle (opcional, máx. 20 palabras)",
        placeholder="Dato complementario — no reemplaza la denominación",
        key="detalle",
    )

st.subheader("Sesión del orden del día")
carga_cs_directa = puede_cargar_cs_directo(ua)
if carga_cs_directa:
    st.success(
        f"**{ua}** puede cargar temas **directamente al orden del día del Consejo Superior**."
    )
else:
    st.caption(
        "Flujo habitual: Consejo Directivo de la UA → aprobación → elevación al CS → revisión de la Secretaría General Académica."
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
    organo_default = organo_default_index(ua_principal, carga_cs_directa)
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
    st.caption(
        "Fechas del **Cronograma Consejo Superior 2026** (fijadas para todo el año). "
        "Elegí la sesión sin consultar el PDF."
    )
    calendario = opciones_fecha_cs(str(anio), sede, incluir_todas=True)
    if not calendario:
        st.warning(f"No hay calendario de Consejo Superior para **{anio}**.")
    else:
        solo_sede = st.checkbox(
            f"Mostrar solo sesiones de **{sede}** + virtuales",
            value=False,
            key="cs_solo_sede",
        )
        if solo_sede:
            calendario = opciones_fecha_cs(str(anio), sede, incluir_todas=False)
        proxima = proxima_fecha_cs(str(anio), sede)
        idx_default = 0
        if proxima:
            et = proxima["opcion"]
            if et in calendario:
                idx_default = calendario.index(et)
        opcion_cs = st.selectbox(
            "Fecha del Consejo Superior *",
            calendario,
            index=idx_default,
            key="fecha_cs",
        )
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

# Contador para reiniciar el uploader al cargar otro tema
_nonce = int(st.session_state.get("lumen_carga_nonce", 0))
archivo_adjunto = render_uploader_adjunto(key=f"carga_{_nonce}")

if st.button("Guardar tema en LUMEN", type="primary"):
    # Leer textos desde session_state (evita perder valor si no se pulsó Enter)
    if not es_inv:
        actividad = str(st.session_state.get("actividad_manual") or "").strip()
        detalle = str(st.session_state.get("detalle") or "").strip()

    errores = []
    if not ua:
        errores.append("Seleccioná la unidad académica.")
    if not actividad or not str(actividad).strip():
        errores.append(
            "Completá **Denominación del tema / actividad** "
            "(el nombre del tema; Detalle es solo un complemento opcional)."
        )
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
        st.session_state["lumen_errores_carga"] = errores
        st.rerun()
    else:
        st.session_state.pop("lumen_errores_carga", None)
        record = {
            "unidad_academica": ua,
            "sede": sede,
            "anio": str(anio),
            "ambito": ambito,
            "es_investigacion": es_inv,
            "tipo_actividad": tipo,
            "tipo_manual": "",
            "actividad": str(actividad).strip(),
            "actividad_manual": True,
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
        con_adjunto = procesar_adjunto_al_guardar(guardado["id"], archivo_adjunto)
        st.session_state["lumen_ultimo_tema_guardado"] = {
            "id": guardado["id"],
            "actividad": guardado.get("actividad", ""),
            "con_adjunto": bool(con_adjunto),
        }
        # Limpiar en el próximo run, antes de crear widgets
        st.session_state["lumen_pendiente_limpiar_tema"] = True
        st.rerun()

# Aviso y acciones al final (después de Guardar)
ultimo = st.session_state.get("lumen_ultimo_tema_guardado")
if ultimo:
    st.markdown("---")
    if ultimo.get("con_adjunto"):
        st.success(
            f"Tema `{ultimo['id']}` registrado **con documento adjunto**. "
            "Formulario listo para el siguiente."
        )
    else:
        st.success(
            f"Tema `{ultimo['id']}` registrado en LUMEN "
            f"(«{ultimo.get('actividad', '')}»). "
            "Formulario listo para el siguiente · el archivo es opcional."
        )
    b_ok1, b_ok2 = st.columns(2)
    with b_ok1:
        st.button(
            "Cargar otro tema",
            type="primary",
            key="btn_cargar_otro_tema",
            on_click=_on_cargar_otro_tema,
            help="Limpia el aviso y deja el formulario listo (UA y fecha se conservan).",
        )
    with b_ok2:
        if not ultimo.get("con_adjunto"):
            if st.button("Ir a Carga de archivos", key="ir_carga_archivos"):
                st.switch_page("pages/5_Carga_Archivos.py")
