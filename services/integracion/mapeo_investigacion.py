"""Mapeo tema LUMEN → fila del sheet Datos Consejo de Investigación."""

from __future__ import annotations

from typing import Any

from services.integracion.config import ModoIntegracion

# Orden de columnas en Hoja 2 (gid 1058037844)
COLUMNAS_CONSEJO = [
    "numero_acta",
    "FECHA",
    "AÑO",
    "TIPO",
    "TITULO",
    "DESCRIPCIÓN",
    "DIRECTOR",
    "CAT_DIRECTOR",
    "CODIRECTOR",
    "CAT_CODIRECTOR",
    "EQUIPO",
    "apellido_nombre_docente",
    "dni_docente",
    "UNIDAD ACADÉMICA",
    "RESOLUCION_CD",
    "RESOLUCION_CS",
    "INSTITUTO",
    "CATEDRA",
    "tipo de financiamiento",
    "Fuente de financiamiento",
    "Monto del financiamiento",
    "ALUMNOS",
    "PUNTAJE",
    "responsable_de_carga",
    "INVESTIGADORES",
    "BECARIOS",
]


def _tipo_investigacion(tema: dict[str, Any]) -> str:
    """Normaliza tipo LUMEN al vocabulario del sheet de Investigación."""
    tipo = (tema.get("tipo_actividad") or "").strip()
    mapa = {
        "Proyecto de investigación": "Proyecto de Investigación",
        "Proyecto de cátedra": "Proyecto de Cátedra",
        "Informe final": "Informe Final",
        "Informe de avance": "Informe de Avance",
        "Categorización docente / investigadores": "Categorización Docente",
        "Semillero de investigación": "Creación de Semillero de Investigación",
        "Jornada / evento académico": "Jornada de Investigación",
        "Líneas prioritarias de investigación": "Líneas prioritarias de investigación",
    }
    for k, v in mapa.items():
        if k.lower() == tipo.lower():
            return v
    return tipo or "Otra"


def fila_consejo_investigacion(tema: dict[str, Any], *, modo: ModoIntegracion | None = None) -> dict[str, Any]:
    """Dict alineado a columnas del sheet productivo de Consejo de Investigación."""
    modo = modo or ModoIntegracion()
    inv = tema.get("investigacion") or {}
    tipo = inv.get("tipo") or _tipo_investigacion(tema)

    anio = tema.get("anio", "")
    anio_cell: Any = int(anio) if str(anio).isdigit() else anio

    fila = {
        "numero_acta": inv.get("numero_acta", tema.get("numero_acta_ci", "")),
        "FECHA": inv.get("fecha_acta", tema.get("fecha_reunion", "")),
        "AÑO": anio_cell,
        "TIPO": tipo,
        "TITULO": inv.get("titulo") or tema.get("actividad", ""),
        "DESCRIPCIÓN": inv.get("descripcion") or tema.get("detalle", ""),
        "DIRECTOR": inv.get("director", ""),
        "CAT_DIRECTOR": inv.get("cat_director", ""),
        "CODIRECTOR": inv.get("codirector", ""),
        "CAT_CODIRECTOR": inv.get("cat_codirector", ""),
        "EQUIPO": inv.get("equipo", ""),
        "apellido_nombre_docente": inv.get("apellido_nombre_docente", ""),
        "dni_docente": inv.get("dni_docente", ""),
        "UNIDAD ACADÉMICA": inv.get("unidades_academicas") or tema.get("unidad_academica", ""),
        "RESOLUCION_CD": inv.get("resolucion_cd", ""),
        "RESOLUCION_CS": inv.get("resolucion_cs", ""),
        "INSTITUTO": inv.get("instituto", ""),
        "CATEDRA": inv.get("catedra", ""),
        "tipo de financiamiento": inv.get("tipo_financiamiento", ""),
        "Fuente de financiamiento": inv.get("fuente_financiamiento", ""),
        "Monto del financiamiento": inv.get("monto_financiamiento", ""),
        "ALUMNOS": inv.get("alumnos", ""),
        "PUNTAJE": inv.get("puntaje", ""),
        "responsable_de_carga": inv.get("responsable_de_carga")
        or tema.get("correo_responsable")
        or modo.correo_responsable_default,
        "INVESTIGADORES": inv.get("investigadores", ""),
        "BECARIOS": inv.get("becarios", ""),
        "ID LUMEN": tema.get("id", ""),
        "Estado LUMEN": tema.get("estado", ""),
        "_destino": "consejo_investigacion",
        "_sheet_id": "17MiyW17W7oLIwSCKjDXCoA85CwBkYqHYhDKblVN37c8",
    }
    fila["_vector"] = [fila.get(c, "") for c in COLUMNAS_CONSEJO]
    return fila


def aplica_a_investigacion(tema: dict[str, Any]) -> bool:
    return bool(tema.get("es_investigacion"))
