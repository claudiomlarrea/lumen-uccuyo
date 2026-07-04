"""Cliente Google Sheets — escritura real solo si LUMEN_SHEETS_LIVE / secrets habilitada."""

from __future__ import annotations

from typing import Any, Literal

from services.integracion.config import (
    CONSEJO_SHEET_ID,
    CONSEJO_WORKSHEET,
    PEI_SHEET_ID,
    ModoIntegracion,
    modo_actual,
)

Destino = Literal["formulario_pei", "consejo_investigacion"]


class IntegracionDesactivadaError(RuntimeError):
    """Se intentó escribir en planillas productivas con la integración apagada."""


def integracion_habilitada(modo: ModoIntegracion | None = None) -> bool:
    return bool((modo or modo_actual()).habilitada)


def append_fila(
    destino: Destino,
    fila: dict[str, Any],
    *,
    modo: ModoIntegracion | None = None,
) -> dict[str, Any]:
    """
    Agrega una fila al sheet productivo.

    Si la integración está desactivada, devuelve simulación sin escribir.
    """
    modo = modo or modo_actual()

    if destino == "formulario_pei":
        sheet_id = PEI_SHEET_ID
        valores = _vector_pei_desde_fila(fila)
        worksheet_hint = "Respuestas de formulario 1"
    else:
        sheet_id = CONSEJO_SHEET_ID
        valores = fila.get("_vector") or []
        worksheet_hint = CONSEJO_WORKSHEET

    if not modo.habilitada:
        return {
            "ok": True,
            "dry_run": True,
            "destino": destino,
            "sheet_id": sheet_id,
            "worksheet": worksheet_hint,
            "valores": valores,
            "mensaje": "Integración desactivada — no se escribió en Google Sheets.",
        }

    return _append_live(destino, sheet_id, worksheet_hint, valores)


def _vector_pei_desde_fila(fila: dict[str, Any]) -> list[Any]:
    indices: dict[int, Any] = fila.get("_vector_indices") or {}
    if not indices:
        return []
    max_idx = max(indices.keys())
    out: list[Any] = [""] * (max_idx + 1)
    for i, v in indices.items():
        out[i] = v
    return out


def _append_live(
    destino: Destino,
    sheet_id: str,
    worksheet_name: str,
    valores: list[Any],
) -> dict[str, Any]:
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        import streamlit as st
    except ImportError as exc:
        raise RuntimeError(
            "Instalá gspread y google-auth, y configurá gcp_service_account en secrets."
        ) from exc

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    book = client.open_by_key(sheet_id)
    try:
        ws = book.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        ws = book.get_worksheet(0)

    ws.append_row(valores, value_input_option="USER_ENTERED")
    return {
        "ok": True,
        "dry_run": False,
        "destino": destino,
        "sheet_id": sheet_id,
        "worksheet": ws.title,
        "filas_agregadas": 1,
    }
