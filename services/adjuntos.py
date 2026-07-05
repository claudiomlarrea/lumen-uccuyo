"""Adjuntos opcionales por tema — prototipo local (futuro: carpetas Google Drive por acta/UA)."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
ADJUNTOS_DIR = ROOT / "data" / "store" / "adjuntos"

EXTENSIONES_PERMITIDAS = (
    "pdf",
    "doc",
    "docx",
    "xls",
    "xlsx",
    "ppt",
    "pptx",
    "jpg",
    "jpeg",
    "png",
)
MAX_BYTES = 10 * 1024 * 1024  # 10 MB — acotado para Streamlit Cloud


def _slug_id(tema_id: str) -> str:
    return re.sub(r"[^\w-]", "_", tema_id)


def _dir_tema(tema_id: str) -> Path:
    return ADJUNTOS_DIR / _slug_id(tema_id)


def _meta_path(tema_id: str) -> Path:
    return _dir_tema(tema_id) / "meta.json"


def validar_archivo(uploaded_file: Any) -> list[str]:
    errores: list[str] = []
    if uploaded_file is None:
        return errores
    nombre = str(getattr(uploaded_file, "name", "") or "")
    ext = nombre.rsplit(".", 1)[-1].lower() if "." in nombre else ""
    if ext not in EXTENSIONES_PERMITIDAS:
        errores.append(
            f"Tipo no permitido (.{ext}). Usá: {', '.join(EXTENSIONES_PERMITIDAS)}."
        )
    tamano = int(getattr(uploaded_file, "size", 0) or 0)
    if tamano > MAX_BYTES:
        errores.append(f"El archivo supera {MAX_BYTES // (1024 * 1024)} MB.")
    return errores


def tiene_adjunto(tema_id: str) -> bool:
    meta = _meta_path(tema_id)
    if not meta.exists():
        return False
    data = json.loads(meta.read_text(encoding="utf-8"))
    archivo = _dir_tema(tema_id) / data.get("nombre_guardado", "")
    return archivo.exists()


def meta_adjunto(tema_id: str) -> dict[str, Any] | None:
    meta = _meta_path(tema_id)
    if not meta.exists():
        return None
    return json.loads(meta.read_text(encoding="utf-8"))


def guardar_adjunto(tema_id: str, uploaded_file: Any) -> dict[str, Any]:
    """Guarda un único adjunto por tema (reemplaza el anterior si existía)."""
    errores = validar_archivo(uploaded_file)
    if errores:
        raise ValueError(errores[0])

    nombre_original = str(uploaded_file.name)
    ext = nombre_original.rsplit(".", 1)[-1].lower()
    nombre_guardado = f"adjunto.{ext}"

    carpeta = _dir_tema(tema_id)
    carpeta.mkdir(parents=True, exist_ok=True)

    # Limpiar archivos previos
    for f in carpeta.iterdir():
        if f.is_file():
            f.unlink()

    destino = carpeta / nombre_guardado
    destino.write_bytes(uploaded_file.getvalue())

    meta: dict[str, Any] = {
        "nombre_original": nombre_original,
        "nombre_guardado": nombre_guardado,
        "mime": str(getattr(uploaded_file, "type", "") or ""),
        "tamano_bytes": destino.stat().st_size,
        "cargado_en": datetime.now().isoformat(timespec="seconds"),
        "opcional": True,
    }
    _meta_path(tema_id).write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta


def leer_adjunto(tema_id: str) -> tuple[bytes, dict[str, Any]] | None:
    meta = meta_adjunto(tema_id)
    if not meta:
        return None
    path = _dir_tema(tema_id) / meta.get("nombre_guardado", "")
    if not path.exists():
        return None
    return path.read_bytes(), meta


def eliminar_adjunto(tema_id: str) -> bool:
    carpeta = _dir_tema(tema_id)
    if not carpeta.exists():
        return False
    for f in carpeta.iterdir():
        if f.is_file():
            f.unlink()
    carpeta.rmdir()
    return True
