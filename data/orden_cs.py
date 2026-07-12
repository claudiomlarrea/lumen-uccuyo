"""Orden y agrupación de temas para el Orden del Día del Consejo Superior."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

# Bloque 1 — carga institucional directa
_UNIDAD_SGA = "Secretaría General Académica"
_UNIDADES_RECTORADO = frozenset(
    {
        "Rectorado",
        "Vicerrector/a",
        "Vicerrector/a de Formación",
        "Vicerrector/a de Sede",
    }
)
_UNIDAD_INVESTIGACION = "Secretaría Investigación"
_UNIDAD_EXTENSION = "Secretaría de Extensión"

# Bloque 5 — unidades académicas por sede (orden San Juan → San Luis → Mendoza)
_UA_SEDE_SAN_JUAN = frozenset(
    {
        "Facultad de Ciencias Médicas San Juan",
        "Facultad de Ciencias Económicas y Empresariales San Juan",
        "Facultad de Derecho y Ciencias Sociales San Juan",
        "Facultad de Filosofía y Humanidades",
        "Facultad de Ciencias Químicas y Tecnológicas",
        "Facultad de Educación",
        "Escuela de Cultura Religiosa y Pastoral",
        "Escuela de Seguridad",
        "Observatorio de Inteligencia Artificial",
        "Departamento de Evaluación y Acreditación",
        "Departamento de Educación a Distancia",
        "Departamento de Graduados",
        "Coordinación General de carreras a distancia",
        "Área de Orientación Universitaria",
    }
)
_UA_SEDE_SAN_LUIS = frozenset(
    {
        "Facultad de Ciencias Médicas San Luis",
        "Facultad de Ciencias Económicas y Empresariales San Luis",
        "Facultad de Derecho y Ciencias Sociales San Luis",
        "Facultad de Ciencias Veterinarias",
        "Instituto de Formación Docentes Santa María",
        "Instituto de Formación Docentes San Buenaventura",
    }
)
_UA_SEDE_MENDOZA = frozenset(
    {
        "Facultad Don Bosco",
    }
)

_TITULOS_GRUPO_CS: dict[str, str] = {
    "Facultad de Ciencias Médicas San Juan": "Facultad de Ciencias Médicas Sede San Juan",
    "Facultad de Ciencias Médicas San Luis": "Facultad de Ciencias Médicas Sede San Luis",
    "Facultad de Ciencias Económicas y Empresariales San Juan": (
        "Facultad de Ciencias Económicas y Empresariales Sede San Juan"
    ),
    "Facultad de Ciencias Económicas y Empresariales San Luis": (
        "Facultad de Ciencias Económicas y Empresariales Sede San Luis"
    ),
    "Facultad de Derecho y Ciencias Sociales San Juan": (
        "Facultad de Derecho y Ciencias Sociales Sede San Juan"
    ),
    "Facultad de Derecho y Ciencias Sociales San Luis": (
        "Facultad de Derecho y Ciencias Sociales Sede San Luis"
    ),
    "Facultad Don Bosco": "Facultad Don Bosco Sede Mendoza",
}


def titulo_encabezado_grupo_cs(unidad_academica: str) -> str:
    """Título visible en Word cuando una UA aporta dos o más temas."""
    ua = str(unidad_academica or "").strip()
    if ua in _TITULOS_GRUPO_CS:
        return _TITULOS_GRUPO_CS[ua]
    if ua.endswith(" San Juan"):
        return ua.replace(" San Juan", " Sede San Juan")
    if ua.endswith(" San Luis"):
        return ua.replace(" San Luis", " Sede San Luis")
    return ua


def _sede_academica(unidad_academica: str, sede_tema: str) -> str:
    ua = str(unidad_academica or "").strip()
    sede = str(sede_tema or "").strip()
    if ua in _UA_SEDE_SAN_JUAN:
        return "San Juan"
    if ua in _UA_SEDE_SAN_LUIS:
        return "San Luis"
    if ua in _UA_SEDE_MENDOZA or sede == "Rodeo del Medio":
        return "Mendoza"
    if sede == "San Luis":
        return "San Luis"
    if sede in {"San Juan", "Inter-sede"}:
        return "San Juan"
    return "Mendoza" if sede == "Rodeo del Medio" else "San Juan"


def _clave_orden_cs(tema: dict[str, Any]) -> tuple[int, int, str, str, str]:
    ua = str(tema.get("unidad_academica") or "").strip()
    sede = _sede_academica(ua, str(tema.get("sede") or ""))

    if ua == _UNIDAD_SGA:
        bloque = 0
    elif ua in _UNIDADES_RECTORADO:
        bloque = 1
    elif ua == _UNIDAD_INVESTIGACION:
        bloque = 2
    elif ua == _UNIDAD_EXTENSION:
        bloque = 3
    else:
        bloque = 4
        orden_sede = {"San Juan": 0, "San Luis": 1, "Mendoza": 2}.get(sede, 9)
        return (
            bloque,
            orden_sede,
            ua.casefold(),
            str(tema.get("actividad") or "").casefold(),
            str(tema.get("id") or ""),
        )

    return (
        bloque,
        0,
        ua.casefold(),
        str(tema.get("actividad") or "").casefold(),
        str(tema.get("id") or ""),
    )


def ordenar_temas_consejo_superior(
    temas: Iterable[dict[str, Any]],
    orden_ua: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Orden del OD del Consejo Superior.

    Si ``orden_ua`` viene de la SGA, los temas se agrupan y ordenan según esa
    secuencia de unidades académicas. Si no, usa el orden institucional por defecto.
    """
    lista = list(temas)
    if orden_ua:
        rank = {ua: i for i, ua in enumerate(orden_ua)}

        def _clave_sga(tema: dict[str, Any]) -> tuple[int, str, str, str]:
            ua = str(tema.get("unidad_academica") or "").strip()
            return (
                rank.get(ua, 10_000),
                ua.casefold(),
                str(tema.get("actividad") or "").casefold(),
                str(tema.get("id") or ""),
            )

        return sorted(lista, key=_clave_sga)
    return sorted(lista, key=_clave_orden_cs)


def orden_ua_institucional(temas: Iterable[dict[str, Any]]) -> list[str]:
    """Lista de UA en el orden institucional por defecto (sin personalizar)."""
    seen: list[str] = []
    for t in sorted(temas, key=_clave_orden_cs):
        ua = str(t.get("unidad_academica") or "").strip()
        if ua and ua not in seen:
            seen.append(ua)
    return seen


def segmentos_grupo_cs(
    temas_ordenados: Iterable[dict[str, Any]],
) -> list[tuple[str | None, list[dict[str, Any]]]]:
    """
    Agrupa temas consecutivos de la misma UA.
    Siempre incluye encabezado de unidad (aunque haya un solo tema).
    """
    segmentos: list[tuple[str | None, list[dict[str, Any]]]] = []
    for tema in temas_ordenados:
        ua = str(tema.get("unidad_academica") or "").strip()
        if segmentos and segmentos[-1][1] and segmentos[-1][1][0].get("unidad_academica") == ua:
            segmentos[-1][1].append(tema)
            continue
        segmentos.append((None, [tema]))

    resultado: list[tuple[str | None, list[dict[str, Any]]]] = []
    for _encabezado, items in segmentos:
        ua = str(items[0].get("unidad_academica") or "").strip()
        resultado.append((titulo_encabezado_grupo_cs(ua), items))
    return resultado
