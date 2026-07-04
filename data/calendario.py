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


def load_calendario_cs(anio: str) -> dict[str, Any] | None:
    path = STORE / f"calendario_cs_{anio}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def reuniones_cs(anio: str) -> list[dict[str, Any]]:
    data = load_calendario_cs(anio)
    if not data:
        return []
    out: list[dict[str, Any]] = []
    for item in data.get("reuniones", []):
        f = _parse_fecha(item["fecha"])
        out.append(
            {
                **item,
                "fecha_iso": item["fecha"],
                "fecha_obj": f,
                "fecha_legible": formato_fecha(f),
            }
        )
    return sorted(out, key=lambda x: x["fecha_obj"])


def fechas_cs_para_sede(anio: str, sede: str, incluir_todas: bool = False) -> list[dict[str, Any]]:
    """Filtra sesiones de CS relevantes para la sede del tema.

    - Presencial en la misma sede.
    - Virtuales (Inter-sede): aplican a todas las UA.
    - Con incluir_todas=True se listan todas las sesiones del año.
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


def opciones_fecha_cs(anio: str, sede: str, incluir_todas: bool = False) -> list[str]:
    return [
        f"{r['fecha_legible']} · {r['etiqueta']}"
        for r in fechas_cs_para_sede(anio, sede, incluir_todas=incluir_todas)
    ]


def fecha_cs_desde_opcion(opcion: str, anio: str) -> dict[str, Any] | None:
    for r in reuniones_cs(anio):
        etiqueta = f"{r['fecha_legible']} · {r['etiqueta']}"
        if etiqueta == opcion:
            return r
    return None


def proxima_fecha_cs(anio: str, sede: str, desde: date | None = None) -> dict[str, Any] | None:
    hoy = desde or date.today()
    candidatas = fechas_cs_para_sede(anio, sede)
    futuras = [r for r in candidatas if r["fecha_obj"] >= hoy]
    return futuras[0] if futuras else None


def etiqueta_organos() -> dict[str, str]:
    return {
        "Consejo Directivo": "CD — fecha definida por la unidad (sin calendario institucional)",
        "Consejo de Investigación": "CI — fecha acordada por Secretaría de Investigación",
        "Consejo de Extensión": "CE — fecha acordada por Secretaría de Extensión",
        "Consejo Superior": "CS — fecha según cronograma anual institucional",
    }
