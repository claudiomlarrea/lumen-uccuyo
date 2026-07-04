"""Mapeo tema LUMEN → fila del Formulario Único PEI (Google Sheet)."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from services.integracion.config import ModoIntegracion

# Índices de columnas (export CSV gid=511573903, jul 2026)
_COL_MARCA = 0
_COL_CORREO = 1
# Por OG n (1..6): objetivo en 2+(n-1)*3, actividad +1, detalle +2
_COL_ANIO = 20
_COL_UNIDAD = 21
_COL_PUNTUACION = 22

PEI_HEADERS_RESUMEN = [
    "Marca temporal",
    "Dirección de correo electrónico",
    "AÑO",
    "Unidad Académica",
    "Objetivo OG activo",
    "Actividad",
    "Detalle",
    "Puntuación",
]


def numero_objetivo_general(objetivo_especifico: str) -> int:
    """Extrae el OG (1–6) desde textos tipo '2.7. Desarrollar programas…'."""
    texto = (objetivo_especifico or "").strip()
    m = re.match(r"^(\d)", texto)
    if m:
        n = int(m.group(1))
        return max(1, min(6, n))
    return 1


def _columna_og(tema: dict[str, Any], campo: str) -> str:
    """Nombre de columna PEI para actividad/detalle/objetivo del OG del tema."""
    og = numero_objetivo_general(tema.get("objetivo_especifico", ""))
    base = 2 + (og - 1) * 3
    if campo == "objetivo":
        return f"Objetivos específicos {og}"
    if campo == "actividad":
        return f"Actividades Objetivo {og}"  # prefijo; el sheet tiene texto largo en cabecera
    if campo == "detalle":
        return f"Detalle de la Actividad Objetivo {og}"
    raise ValueError(campo)


def fila_formulario_pei(tema: dict[str, Any], *, modo: ModoIntegracion | None = None) -> dict[str, Any]:
    """
    Devuelve un dict legible para simulación y un vector alineado a columnas PEI.

    Solo llena el bloque del objetivo general que corresponde al tema.
    """
    modo = modo or ModoIntegracion()
    og = numero_objetivo_general(tema.get("objetivo_especifico", ""))
    inv = tema.get("investigacion") or {}
    puntaje = inv.get("puntaje", tema.get("puntuacion_pei", ""))

    legible = {
        "Marca temporal": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "Dirección de correo electrónico": tema.get("correo_responsable") or modo.correo_responsable_default,
        "AÑO": tema.get("anio", ""),
        "Unidad Académica": tema.get("unidad_academica", ""),
        "Objetivo OG activo": og,
        "Objetivo específico": tema.get("objetivo_especifico", ""),
        "Actividad": tema.get("actividad", ""),
        "Detalle": tema.get("detalle", ""),
        "Puntuación": puntaje,
        "ID LUMEN": tema.get("id", ""),
        "Estado LUMEN": tema.get("estado", ""),
    }

    # Vector disperso: índice → valor (para append por posición cuando se active gspread)
    vector: dict[int, Any] = {
        _COL_MARCA: legible["Marca temporal"],
        _COL_CORREO: legible["Dirección de correo electrónico"],
        _COL_ANIO: int(tema["anio"]) if str(tema.get("anio", "")).isdigit() else tema.get("anio", ""),
        _COL_UNIDAD: legible["Unidad Académica"],
    }
    if puntaje not in (None, ""):
        vector[_COL_PUNTUACION] = puntaje

    idx_obj = 2 + (og - 1) * 3
    vector[idx_obj] = tema.get("objetivo_especifico", "")
    vector[idx_obj + 1] = tema.get("actividad", "")
    vector[idx_obj + 2] = tema.get("detalle", "")

    legible["_vector_indices"] = vector
    legible["_destino"] = "formulario_pei"
    legible["_sheet_id"] = "1c-ZPobdyqA5pW9mhyJsC1uJwFFAcEv4HliOjcSwhOsg"
    return legible


def aplica_a_pei(tema: dict[str, Any]) -> bool:
    return bool(tema.get("impacta_pei"))
