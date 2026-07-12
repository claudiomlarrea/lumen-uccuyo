"""Orden de unidades académicas en el OD del Consejo Superior (elige la SGA)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "store"
ORDEN_PATH = DATA_DIR / "orden_ua_cs.json"
_SESSION_ORDEN = "lumen_orden_ua_cs"


def _clave(anio: str, fecha_legible: str) -> str:
    return f"{anio}|{fecha_legible}"


def _ensure() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not ORDEN_PATH.exists():
        ORDEN_PATH.write_text("{}", encoding="utf-8")


def _leer_disco() -> dict[str, list[str]]:
    _ensure()
    try:
        data = json.loads(ORDEN_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _store() -> dict[str, list[str]]:
    try:
        import streamlit as st

        if _SESSION_ORDEN not in st.session_state:
            st.session_state[_SESSION_ORDEN] = _leer_disco()
        return st.session_state[_SESSION_ORDEN]
    except Exception:
        return _leer_disco()


def load_orden_ua_cs(anio: str, fecha_legible: str) -> list[str]:
    """Orden de UA guardado para una sesión CS (puede estar vacío)."""
    return list(_store().get(_clave(anio, fecha_legible), []))


def save_orden_ua_cs(anio: str, fecha_legible: str, unidades: list[str]) -> None:
    store = _store()
    store[_clave(anio, fecha_legible)] = list(unidades)
    try:
        import streamlit as st

        st.session_state[_SESSION_ORDEN] = store
    except Exception:
        pass
    _ensure()
    ORDEN_PATH.write_text(json.dumps(store, ensure_ascii=False, indent=2), encoding="utf-8")


def unidades_presentes(temas: list[dict[str, Any]]) -> list[str]:
    """UA distintas en el orden en que aparecen los temas (sin reordenar)."""
    seen: list[str] = []
    for t in temas:
        ua = str(t.get("unidad_academica") or "").strip()
        if ua and ua not in seen:
            seen.append(ua)
    return seen


def resolver_orden_ua(
    anio: str,
    fecha_legible: str,
    temas: list[dict[str, Any]],
    *,
    orden_institucional: list[str] | None = None,
) -> list[str]:
    """
    Combina el orden elegido por SGA con las UA que hoy tienen temas en la sesión.
    Conserva el orden guardado; agrega UA nuevas al final (según orden institucional si hay).
    """
    actuales = set(unidades_presentes(temas))
    if not actuales:
        return []

    guardado = load_orden_ua_cs(anio, fecha_legible)
    resultado = [u for u in guardado if u in actuales]

    restantes = [u for u in actuales if u not in resultado]
    if orden_institucional:
        resto_ord = [u for u in orden_institucional if u in restantes]
        resto_ord += sorted(u for u in restantes if u not in resto_ord)
        resultado.extend(resto_ord)
    else:
        resultado.extend(sorted(restantes))

    return resultado
