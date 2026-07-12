"""Calendario institucional de reuniones de órganos de gobierno (prototipo LUMEN)."""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
STORE = ROOT / "store"

ORGANOS_TRATAMIENTO = [
    "Consejo Directivo",
    "Consejo de Investigación",
    "Consejo de Extensión",
    "Consejo Superior",
]

ORGANOS_FECHA_LIBRE = {
    "Consejo Directivo",
    "Consejo de Investigación",
    "Consejo de Extensión",
}

ORGANOS_ELEVABLES_A_CS = ORGANOS_FECHA_LIBRE

ORGANO_DEFAULT_POR_UA = {
    "Secretaría Investigación": "Consejo de Investigación",
    "Secretaría de Extensión": "Consejo de Extensión",
}

SEDES_CS = ["San Juan", "San Luis", "Rodeo del Medio", "Inter-sede"]

# Cronograma oficial CS 2026 (PDF: Cronograma Consejo Superior 2026.pdf)
# Misma lógica que las fechas fijas de actas en Consejo de Investigación:
# el usuario elige de esta lista, sin consultar el calendario aparte.
REUNIONES_CS_FIJAS: dict[str, list[dict[str, str]]] = {
    "2026": [
        {
            "fecha": "2026-02-27",
            "sede": "San Juan",
            "modalidad": "presencial",
            "etiqueta": "Consejo Superior — San Juan",
        },
        {
            "fecha": "2026-03-27",
            "sede": "Inter-sede",
            "modalidad": "virtual",
            "etiqueta": "Consejo Superior — Virtual",
        },
        {
            "fecha": "2026-04-24",
            "sede": "Rodeo del Medio",
            "modalidad": "presencial",
            "etiqueta": "Consejo Superior — Rodeo del Medio",
        },
        {
            "fecha": "2026-05-29",
            "sede": "Inter-sede",
            "modalidad": "virtual",
            "etiqueta": "Consejo Superior — Virtual",
        },
        {
            "fecha": "2026-06-26",
            "sede": "San Luis",
            "modalidad": "presencial",
            "etiqueta": "Consejo Superior — San Luis",
        },
        {
            "fecha": "2026-07-31",
            "sede": "Inter-sede",
            "modalidad": "virtual",
            "etiqueta": "Consejo Superior — Virtual",
        },
        {
            "fecha": "2026-08-28",
            "sede": "San Juan",
            "modalidad": "presencial",
            "etiqueta": "Consejo Superior — San Juan",
        },
        {
            "fecha": "2026-09-25",
            "sede": "Inter-sede",
            "modalidad": "virtual",
            "etiqueta": "Consejo Superior — Virtual",
        },
        {
            "fecha": "2026-10-30",
            "sede": "San Luis",
            "modalidad": "presencial",
            "etiqueta": "Consejo Superior — San Luis",
        },
        {
            "fecha": "2026-11-27",
            "sede": "Inter-sede",
            "modalidad": "virtual",
            "etiqueta": "Consejo Superior — Virtual",
        },
        {
            "fecha": "2026-12-18",
            "sede": "San Juan",
            "modalidad": "presencial",
            "etiqueta": "Consejo Superior — San Juan",
        },
    ],
}


def usa_calendario_cs(organo: str) -> bool:
    return organo == "Consejo Superior"


def usa_fecha_libre(organo: str) -> bool:
    return organo in ORGANOS_FECHA_LIBRE


def organo_default_index(ua: str, carga_cs_directa: bool) -> int:
    if carga_cs_directa:
        return ORGANOS_TRATAMIENTO.index("Consejo Superior")
    preferido = ORGANO_DEFAULT_POR_UA.get(ua, "Consejo Directivo")
    return ORGANOS_TRATAMIENTO.index(preferido)


def _parse_fecha(val: str) -> date:
    return datetime.strptime(val, "%Y-%m-%d").date()


def formato_fecha(val: date) -> str:
    dias = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
    meses = [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    ]
    return f"{dias[val.weekday()]} {val.day} de {meses[val.month - 1]} de {val.year}"


def _etiqueta_opcion(reunion: dict[str, Any]) -> str:
    """Texto del desplegable: fecha + sede/modalidad (estilo actas CI)."""
    sede = reunion.get("sede", "")
    modalidad = reunion.get("modalidad", "")
    if modalidad == "virtual":
        lugar = "Virtual (todas las sedes)"
    else:
        lugar = sede
    return f"{reunion['fecha_legible']} — {lugar}"


def load_calendario_cs(anio: str) -> dict[str, Any] | None:
    """Prioriza JSON en store; si no hay, usa el cronograma embebido."""
    path = STORE / f"calendario_cs_{anio}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    fijas = REUNIONES_CS_FIJAS.get(anio)
    if not fijas:
        return None
    return {
        "anio": anio,
        "organismo": "consejo_superior",
        "fuente": "Cronograma Consejo Superior 2026.pdf (embebido)",
        "reuniones": fijas,
    }


def reuniones_cs(anio: str) -> list[dict[str, Any]]:
    data = load_calendario_cs(anio)
    if not data:
        return []
    out: list[dict[str, Any]] = []
    for item in data.get("reuniones", []):
        f = _parse_fecha(item["fecha"])
        reunion = {
            **item,
            "fecha_iso": item["fecha"],
            "fecha_obj": f,
            "fecha_legible": formato_fecha(f),
        }
        reunion["opcion"] = _etiqueta_opcion(reunion)
        out.append(reunion)
    return sorted(out, key=lambda x: x["fecha_obj"])


def fechas_cs_para_sede(anio: str, sede: str, incluir_todas: bool = True) -> list[dict[str, Any]]:
    """Sesiones de CS del cronograma anual.

    Por defecto incluye todas (como el desplegable de actas del CI).
    Si incluir_todas=False, filtra presencial de la sede + virtuales.
    """
    reuniones = reuniones_cs(anio)
    if incluir_todas or sede == "Inter-sede":
        return reuniones

    filtradas: list[dict[str, Any]] = []
    for r in reuniones:
        if r.get("modalidad") == "virtual":
            filtradas.append(r)
        elif r.get("sede") == sede:
            filtradas.append(r)
    return filtradas


def opciones_fecha_cs(anio: str, sede: str, incluir_todas: bool = True) -> list[str]:
    return [r["opcion"] for r in fechas_cs_para_sede(anio, sede, incluir_todas=incluir_todas)]


def fecha_cs_desde_opcion(opcion: str, anio: str) -> dict[str, Any] | None:
    for r in reuniones_cs(anio):
        if r["opcion"] == opcion:
            return r
        # Compatibilidad con formato anterior
        legacy = f"{r['fecha_legible']} · {r['etiqueta']}"
        if legacy == opcion:
            return r
    return None


def proxima_fecha_cs(anio: str, sede: str, desde: date | None = None) -> dict[str, Any] | None:
    hoy = desde or date.today()
    candidatas = fechas_cs_para_sede(anio, sede, incluir_todas=True)
    futuras = [r for r in candidatas if r["fecha_obj"] >= hoy]
    return futuras[0] if futuras else None


def etiqueta_organos() -> dict[str, str]:
    return {
        "Consejo Directivo": "CD — fecha definida por la unidad (sin calendario institucional)",
        "Consejo de Investigación": "CI — fecha acordada por Secretaría de Investigación",
        "Consejo de Extensión": "CE — fecha acordada por Secretaría de Extensión",
        "Consejo Superior": "CS — fecha según cronograma anual institucional",
    }
