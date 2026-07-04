"""Configuración de planillas productivas y modo de publicación."""

from __future__ import annotations

import os
from dataclasses import dataclass

# Formulario Único PEI → Tablero Looker PEI
PEI_SHEET_ID = "1c-ZPobdyqA5pW9mhyJsC1uJwFFAcEv4HliOjcSwhOsg"
PEI_SHEET_GID = 511573903
PEI_SHEET_NAME = "Respuestas de formulario 1"  # nombre habitual; se valida al conectar

# Datos Consejo de Investigación → Tablero Plan Estratégico de Investigación
CONSEJO_SHEET_ID = "17MiyW17W7oLIwSCKjDXCoA85CwBkYqHYhDKblVN37c8"
CONSEJO_SHEET_GID = 1058037844
CONSEJO_WORKSHEET = "Hoja 2"

PEI_LOOKER_URL = (
    "https://datastudio.google.com/u/1/reporting/"
    "1402e4de-9e87-4543-b7f3-4ba714819429/page/p_2mexfiotmd"
)
INVESTIGACION_LOOKER_URL = (
    "https://datastudio.google.com/u/1/reporting/"
    "42923975-d3ff-4972-acd7-ab51db384f13/page/p_xtiikpfv2d"
)

PEI_FORM_URL = f"https://docs.google.com/spreadsheets/d/{PEI_SHEET_ID}/edit#gid={PEI_SHEET_GID}"
CONSEJO_FORM_URL = f"https://docs.google.com/spreadsheets/d/{CONSEJO_SHEET_ID}/edit#gid={CONSEJO_SHEET_GID}"

ESTADOS_PUBLICABLES_PEI = frozenset({"aprobado_cd", "aprobado_cs", "publicado_simulado"})
ESTADOS_PUBLICABLES_INVESTIGACION = frozenset(
    {"aprobado_cd", "aprobado_cs", "publicado_simulado", "en_orden_del_dia", "en_orden_del_dia_cs"}
)


@dataclass(frozen=True)
class ModoIntegracion:
    """Control de escritura en planillas productivas."""

    habilitada: bool = False
    correo_responsable_default: str = "prototipo.lumen@uccuyo.edu.ar"

    @classmethod
    def desde_entorno(cls) -> ModoIntegracion:
        flag = os.environ.get("LUMEN_SHEETS_LIVE", "").strip().lower() in {"1", "true", "yes"}
        return cls(habilitada=flag)

    @classmethod
    def desde_streamlit(cls) -> ModoIntegracion:
        try:
            import streamlit as st

            cfg = st.secrets.get("lumen_integracion", {})
            habilitada = bool(cfg.get("habilitada", False))
            correo = str(cfg.get("correo_responsable_default", cls.correo_responsable_default))
            return cls(habilitada=habilitada, correo_responsable_default=correo)
        except Exception:
            return cls.desde_entorno()


def modo_actual() -> ModoIntegracion:
    """Prioridad: secrets Streamlit → variable de entorno → apagado."""
    try:
        import streamlit as st

        if hasattr(st, "secrets"):
            return ModoIntegracion.desde_streamlit()
    except Exception:
        pass
    return ModoIntegracion.desde_entorno()
