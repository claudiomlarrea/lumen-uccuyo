"""Almacenamiento local del prototipo LUMEN (JSON). No escribe en Google Sheets."""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from data.calendario import ORGANOS_ELEVABLES_A_CS

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "store"
TEMAS_PATH = DATA_DIR / "temas.json"
CATALOGO_MANUAL_PATH = DATA_DIR / "catalogo_manual.json"


def _ensure() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not TEMAS_PATH.exists():
        TEMAS_PATH.write_text("[]", encoding="utf-8")
    if not CATALOGO_MANUAL_PATH.exists():
        CATALOGO_MANUAL_PATH.write_text(
            json.dumps({"tipos": [], "actividades_por_ua": {}}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def load_temas() -> list[dict[str, Any]]:
    _ensure()
    return json.loads(TEMAS_PATH.read_text(encoding="utf-8"))


def save_temas(temas: list[dict[str, Any]]) -> None:
    _ensure()
    TEMAS_PATH.write_text(json.dumps(temas, ensure_ascii=False, indent=2), encoding="utf-8")


def load_catalogo_manual() -> dict[str, Any]:
    _ensure()
    return json.loads(CATALOGO_MANUAL_PATH.read_text(encoding="utf-8"))


def save_catalogo_manual(data: dict[str, Any]) -> None:
    _ensure()
    CATALOGO_MANUAL_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def nuevo_id() -> str:
    return f"LUMEN-{datetime.now():%Y%m%d}-{uuid.uuid4().hex[:6].upper()}"


def agregar_tema(tema: dict[str, Any]) -> dict[str, Any]:
    temas = load_temas()
    tema = {
        "id": nuevo_id(),
        "creado_en": datetime.now().isoformat(timespec="seconds"),
        "estado": tema.get("estado", "en_orden_del_dia"),
        "publicado_pei_simulado": False,
        "publicado_investigacion_simulado": False,
        **tema,
    }
    temas.append(tema)
    save_temas(temas)

    # Enriquecer catálogo manual si hubo carga a mano
    cat = load_catalogo_manual()
    if tema.get("tipo_manual"):
        if tema["tipo_manual"] not in cat["tipos"]:
            cat["tipos"].append(tema["tipo_manual"])
    ua = tema.get("unidad_academica", "")
    act = tema.get("actividad", "")
    if tema.get("actividad_manual") and ua and act:
        cat.setdefault("actividades_por_ua", {}).setdefault(ua, [])
        if act not in cat["actividades_por_ua"][ua]:
            cat["actividades_por_ua"][ua].append(act)
    save_catalogo_manual(cat)
    return tema


def actualizar_tema(tema_id: str, cambios: dict[str, Any]) -> dict[str, Any] | None:
    temas = load_temas()
    for i, t in enumerate(temas):
        if t["id"] == tema_id:
            temas[i] = {**t, **cambios, "actualizado_en": datetime.now().isoformat(timespec="seconds")}
            save_temas(temas)
            return temas[i]
    return None


def eliminar_tema(tema_id: str) -> bool:
    temas = load_temas()
    nuevos = [t for t in temas if t["id"] != tema_id]
    if len(nuevos) == len(temas):
        return False
    save_temas(nuevos)
    return True


def elevar_tema_a_cs(tema_id: str, reunion_cs: dict[str, Any]) -> dict[str, Any] | None:
    """Eleva un tema aprobado en CD/CI/CE al Consejo Superior (bandeja SGA)."""
    temas = load_temas()
    for i, t in enumerate(temas):
        if t["id"] != tema_id:
            continue
        organo = t.get("organo_tratamiento", "")
        if organo not in ORGANOS_ELEVABLES_A_CS:
            raise ValueError("Solo se elevan temas de Consejo Directivo, de Investigación o de Extensión.")
        if t.get("estado") != "aprobado_cd":
            raise ValueError(f"El tema debe estar aprobado en {organo} antes de elevarlo.")
        temas[i] = {
            **t,
            "estado": "pendiente_revision_sga",
            "elevado_desde_cd": True,
            "organo_origen": organo,
            "fecha_cd": t.get("fecha_reunion", ""),
            "fecha_cd_iso": t.get("fecha_reunion_iso", ""),
            "organo_tratamiento": "Consejo Superior",
            "requiere_cs": "Sí",
            "fecha_reunion": reunion_cs.get("fecha_legible", ""),
            "fecha_reunion_iso": reunion_cs.get("fecha_iso", ""),
            "cs_sede_reunion": reunion_cs.get("sede", ""),
            "cs_modalidad": reunion_cs.get("modalidad", ""),
            "elevado_en": datetime.now().isoformat(timespec="seconds"),
            "actualizado_en": datetime.now().isoformat(timespec="seconds"),
        }
        save_temas(temas)
        return temas[i]
    return None


def incorporar_tema_cs(tema_id: str) -> dict[str, Any] | None:
    """Secretaría General Académica incorpora el tema al orden del día del CS."""
    return actualizar_tema(
        tema_id,
        {
            "estado": "en_orden_del_dia_cs",
            "revisado_sga_en": datetime.now().isoformat(timespec="seconds"),
        },
    )


def devolver_tema_a_cd(tema_id: str, observacion: str = "") -> dict[str, Any] | None:
    """SGA devuelve un tema elevado a la unidad de origen."""
    temas = load_temas()
    for i, t in enumerate(temas):
        if t["id"] != tema_id:
            continue
        cambios: dict[str, Any] = {
            "estado": "aprobado_cd",
            "organo_tratamiento": t.get("organo_origen", "Consejo Directivo"),
            "fecha_reunion": t.get("fecha_cd", t.get("fecha_reunion", "")),
            "fecha_reunion_iso": t.get("fecha_cd_iso", t.get("fecha_reunion_iso", "")),
            "elevado_desde_cd": False,
            "devuelto_sga_en": datetime.now().isoformat(timespec="seconds"),
        }
        if observacion.strip():
            cambios["observacion_sga"] = observacion.strip()
        temas[i] = {**t, **cambios, "actualizado_en": datetime.now().isoformat(timespec="seconds")}
        save_temas(temas)
        return temas[i]
    return None


def actividades_para_ua(ua: str, base: dict[str, list[str]]) -> list[str]:
    cat = load_catalogo_manual()
    manuales = cat.get("actividades_por_ua", {}).get(ua, [])
    semilla = base.get(ua, [])
    # unir preservando orden
    seen: set[str] = set()
    out: list[str] = []
    for item in semilla + manuales:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def tipos_extra() -> list[str]:
    cat = load_catalogo_manual()
    return cat.get("tipos", [])
