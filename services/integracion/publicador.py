"""Orquestación de publicación LUMEN → PEI + Consejo de Investigación."""

from __future__ import annotations

from typing import Any, Literal

from services.integracion.config import (
    ESTADOS_PUBLICABLES_INVESTIGACION,
    ESTADOS_PUBLICABLES_PEI,
    ModoIntegracion,
    modo_actual,
)
from services.integracion.mapeo_investigacion import aplica_a_investigacion, fila_consejo_investigacion
from services.integracion.mapeo_pei import aplica_a_pei, fila_formulario_pei
from services.integracion.sheets_client import append_fila

Destino = Literal["formulario_pei", "consejo_investigacion"]


def es_publicable_pei(tema: dict[str, Any]) -> bool:
    return aplica_a_pei(tema) and tema.get("estado") in ESTADOS_PUBLICABLES_PEI


def es_publicable_investigacion(tema: dict[str, Any]) -> bool:
    return aplica_a_investigacion(tema) and tema.get("estado") in ESTADOS_PUBLICABLES_INVESTIGACION


def destinos_de_tema(tema: dict[str, Any]) -> list[Destino]:
    """Destinos productivos según reglas institucionales."""
    out: list[Destino] = []
    if es_publicable_pei(tema):
        out.append("formulario_pei")
    if es_publicable_investigacion(tema):
        out.append("consejo_investigacion")
    return out


def resumen_publicacion(temas: list[dict[str, Any]]) -> dict[str, int]:
    solo_pei = solo_inv = ambos = 0
    for t in temas:
        d = set(destinos_de_tema(t))
        if not d:
            continue
        if d == {"formulario_pei", "consejo_investigacion"}:
            ambos += 1
        elif "formulario_pei" in d:
            solo_pei += 1
        elif "consejo_investigacion" in d:
            solo_inv += 1
    return {
        "total_temas": len(temas),
        "publicables_pei": sum(1 for t in temas if es_publicable_pei(t)),
        "publicables_investigacion": sum(1 for t in temas if es_publicable_investigacion(t)),
        "solo_pei": solo_pei,
        "solo_investigacion": solo_inv,
        "pei_e_investigacion": ambos,
    }


def publicar_tema(
    tema: dict[str, Any],
    *,
    modo: ModoIntegracion | None = None,
    forzar: bool = False,
) -> list[dict[str, Any]]:
    """Publica un tema en todos los destinos que correspondan."""
    modo = modo or modo_actual()
    resultados: list[dict[str, Any]] = []

    if aplica_a_pei(tema) and (forzar or es_publicable_pei(tema)):
        fila = fila_formulario_pei(tema, modo=modo)
        resultados.append(append_fila("formulario_pei", fila, modo=modo))

    if aplica_a_investigacion(tema) and (forzar or es_publicable_investigacion(tema)):
        fila = fila_consejo_investigacion(tema, modo=modo)
        resultados.append(append_fila("consejo_investigacion", fila, modo=modo))

    return resultados


def publicar_temas(
    temas: list[dict[str, Any]],
    *,
    modo: ModoIntegracion | None = None,
) -> dict[str, Any]:
    """Publica lote; nunca escribe si integración desactivada."""
    modo = modo or modo_actual()
    detalle: list[dict[str, Any]] = []
    filas_pei = 0
    filas_inv = 0

    for tema in temas:
        destinos = destinos_de_tema(tema)
        if not destinos:
            continue
        for res in publicar_tema(tema, modo=modo):
            detalle.append({"tema_id": tema.get("id"), **res})
            if res.get("destino") == "formulario_pei":
                filas_pei += 1
            elif res.get("destino") == "consejo_investigacion":
                filas_inv += 1

    return {
        "habilitada": modo.habilitada,
        "dry_run": not modo.habilitada,
        "filas_pei": filas_pei,
        "filas_investigacion": filas_inv,
        "detalle": detalle,
    }
