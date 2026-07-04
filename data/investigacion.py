"""Catálogos y reglas del formulario Consejo de Investigación en LUMEN."""

from __future__ import annotations

import re
import unicodedata
from typing import Any

# Tipos alineados al sistema productivo (Consejo de Investigación)
TIPOS_CI = [
    "Proyecto de Investigación",
    "Proyecto de Cátedra",
    "Informe Final",
    "Informe de Avance",
    "Jornada de Investigación",
    "Convocatoria a Proyectos de investigación",
    "Creación de Semillero de Investigación",
    "Categorización Docente",
    "Llamado a Concurso de Becas",
    "Líneas prioritarias de investigación",
    "Otra",
]

TIPOS_CON_PUNTAJE = frozenset(
    {
        "Proyecto de Investigación",
        "Proyecto de Cátedra",
        "Informe Final",
        "Informe de Avance",
    }
)

TIPOS_CON_EQUIPO = frozenset(
    {
        "Proyecto de Investigación",
        "Proyecto de Cátedra",
        "Informe Final",
        "Informe de Avance",
        "Otra",
    }
)

CATEGORIAS_INVESTIGADOR = [
    "Seleccionar",
    "Investigador/a Superior I",
    "Investigador/a Principal II",
    "Investigador/a Independiente III",
    "Investigador/a Adjunto/a IV",
    "Investigador/a Asistente V",
    "Becario/a de Iniciación VI",
    "Sin categorización / Externo",
]

TIPOS_FINANCIAMIENTO = ["Seleccionar...", "Interno", "Externo", "Sin financiamiento"]

# Actas CI 2026 (referencia del sistema productivo)
ACTAS_CI_2026: dict[int, str] = {
    187: "19 de Febrero 2026",
    188: "19 de Marzo 2026",
    189: "16 de Abril 2026",
    190: "21 de Mayo 2026",
    191: "18 de Junio 2026",
    192: "23 de Julio 2026",
    193: "20 de Agosto 2026",
    194: "15 de Septiembre 2026",
    195: "22 de Octubre 2026",
    196: "19 de Noviembre 2026",
    197: "10 de Diciembre 2026",
}


MAX_UNIDADES_ACADEMICAS = 5

# Unidades elegibles en carga CI (facultades, escuelas, institutos — no órganos de gobierno)
UNIDADES_CI = [
    "Facultad de Ciencias Médicas San Juan",
    "Facultad de Ciencias Médicas San Luis",
    "Facultad de Ciencias Económicas y Empresariales San Juan",
    "Facultad de Ciencias Económicas y Empresariales San Luis",
    "Facultad de Derecho y Ciencias Sociales San Juan",
    "Facultad de Derecho y Ciencias Sociales San Luis",
    "Facultad de Filosofía y Humanidades",
    "Facultad de Ciencias Químicas y Tecnológicas",
    "Facultad de Educación",
    "Facultad de Ciencias Veterinarias",
    "Facultad Don Bosco",
    "Escuela de Cultura Religiosa y Pastoral",
    "Escuela de Seguridad",
    "Instituto de Formación Docentes Santa María",
    "Instituto de Formación Docentes San Buenaventura",
    "Secretaría Investigación",
    "Observatorio de Inteligencia Artificial",
    "Departamento de Educación a Distancia",
    "Vicerrector/a de Formación",
]


def contar_palabras(texto: str) -> int:
    return len(re.findall(r"\S+", str(texto or "").strip()))


def limpiar_seleccionar(valor: str) -> str:
    v = str(valor or "").strip()
    if not v or v.startswith("Seleccionar"):
        return ""
    return v


def _normalizar_puntaje_num(x: float) -> float:
    if x != x or x <= 0:
        return x
    while x > 1000 and abs(x - round(x)) < 1e-4:
        ri = int(round(x))
        if ri % 100 != 0:
            break
        x = x / 100.0
    return x


def parse_puntaje(val: Any) -> float | None:
    if val is None or val == "":
        return None
    if isinstance(val, (int, float)):
        x = float(val)
        return None if x != x else _normalizar_puntaje_num(x)
    s = unicodedata.normalize("NFKC", str(val))
    s = re.sub(r"\s+", "", s)
    if not s:
        return None
    m = re.match(r"^(\d{1,4})([.,])(\d{1,4})$", s)
    if m:
        whole, _sep, frac = m.groups()
        try:
            return _normalizar_puntaje_num(float(f"{whole}.{frac}"))
        except ValueError:
            return None
    s = s.replace(",", ".")
    try:
        return _normalizar_puntaje_num(float(s))
    except ValueError:
        return None


def puntaje_para_sheet(val: Any) -> str:
    n = parse_puntaje(val)
    if n is None or n <= 0:
        return ""
    if abs(n - round(n)) < 1e-9:
        return str(int(round(n)))
    return f"{n:.4f}".rstrip("0").rstrip(".")


def requiere_equipo(tipo_ci: str) -> bool:
    return tipo_ci in TIPOS_CON_EQUIPO


def requiere_puntaje(tipo_ci: str) -> bool:
    return tipo_ci in TIPOS_CON_PUNTAJE


def es_categorizacion(tipo_ci: str) -> bool:
    return tipo_ci == "Categorización Docente"


def validar_campos_investigacion(tipo_ci: str, data: dict[str, Any]) -> list[str]:
    errores: list[str] = []
    titulo = str(data.get("titulo") or data.get("denominacion") or "").strip()
    if not titulo:
        errores.append("Completá la denominación del tema de investigación.")
    desc = str(data.get("descripcion") or "")
    if contar_palabras(desc) > 50:
        errores.append("La descripción no puede superar 50 palabras.")
    if requiere_puntaje(tipo_ci):
        raw = data.get("puntaje_raw", "")
        if raw and parse_puntaje(raw) is None:
            errores.append("Puntaje inválido. Usá coma o punto (ej: 87,9).")
    if requiere_equipo(tipo_ci):
        eq = str(data.get("equipo") or "")
        if contar_palabras(eq) > 50:
            errores.append("El equipo no puede superar 50 palabras.")
    unidades = data.get("unidades_academicas") or []
    if not unidades:
        errores.append("Seleccioná al menos una unidad académica.")
    elif len(unidades) > MAX_UNIDADES_ACADEMICAS:
        errores.append(f"Solo podés elegir hasta {MAX_UNIDADES_ACADEMICAS} unidades académicas.")
    return errores


def armar_bloque_investigacion(tipo_ci: str, raw: dict[str, Any]) -> dict[str, Any]:
    """Normaliza campos del formulario al bloque JSON `investigacion`."""
    puntaje_val = parse_puntaje(raw.get("puntaje_raw")) if requiere_puntaje(tipo_ci) else None
    monto = raw.get("monto_financiamiento")
    if monto is None:
        monto = ""

    bloque: dict[str, Any] = {
        "tipo": tipo_ci,
        "titulo": str(raw.get("titulo") or "").strip(),
        "descripcion": str(raw.get("descripcion") or "").strip(),
        "numero_acta": raw.get("numero_acta", ""),
        "fecha_acta": raw.get("fecha_acta", ""),
        "responsable_de_carga": str(raw.get("responsable_de_carga") or "").strip(),
    }

    if es_categorizacion(tipo_ci):
        bloque.update(
            {
                "apellido_nombre_docente": str(raw.get("apellido_nombre_docente") or "").strip(),
                "dni_docente": str(raw.get("dni_docente") or "").strip(),
            }
        )
        unidades = raw.get("unidades_academicas") or []
        if unidades:
            bloque["unidades_academicas"] = "; ".join(unidades)
        return bloque

    if requiere_equipo(tipo_ci):
        bloque.update(
            {
                "director": str(raw.get("director") or "").strip(),
                "cat_director": limpiar_seleccionar(str(raw.get("cat_director") or "")),
                "codirector": str(raw.get("codirector") or "").strip(),
                "cat_codirector": limpiar_seleccionar(str(raw.get("cat_codirector") or "")),
                "equipo": str(raw.get("equipo") or "").strip(),
                "instituto": limpiar_seleccionar(str(raw.get("instituto") or "")),
                "catedra": str(raw.get("catedra") or "").strip(),
                "alumnos": str(raw.get("alumnos") or "").strip(),
                "resolucion_cd": str(raw.get("resolucion_cd") or "").strip(),
                "resolucion_cs": str(raw.get("resolucion_cs") or "").strip(),
            }
        )

    if puntaje_val is not None and puntaje_val > 0:
        bloque["puntaje"] = puntaje_para_sheet(puntaje_val)

    bloque.update(
        {
            "tipo_financiamiento": limpiar_seleccionar(str(raw.get("tipo_financiamiento") or "")),
            "fuente_financiamiento": str(raw.get("fuente_financiamiento") or "").strip(),
            "monto_financiamiento": monto,
        }
    )
    unidades = raw.get("unidades_academicas") or []
    if unidades:
        bloque["unidades_academicas"] = "; ".join(unidades)
    return bloque
