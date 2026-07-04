"""Generación del Orden del Día en Word (prototipo local)."""

from __future__ import annotations

import re
import unicodedata
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "assets" / "logo_uccuyo_white.png"

VERDE = RGBColor(0x00, 0x4D, 0x2C)
ROJO = RGBColor(0x8B, 0x1E, 0x2D)


def _slug(texto: str) -> str:
    """Nombre de archivo seguro (ASCII) para evitar descargas sin extensión en Edge/Chrome."""
    nfkd = unicodedata.normalize("NFKD", texto)
    ascii_text = nfkd.encode("ascii", "ignore").decode("ascii")
    limpio = re.sub(r"[^\w-]", "_", ascii_text)
    limpio = re.sub(r"_+", "_", limpio).strip("_")
    return (limpio or "documento")[:50]


from data.investigacion import parse_puntaje

TIPOS_CON_DIRECTOR = frozenset(
    {
        "Proyecto de Investigación",
        "Proyecto de Cátedra",
        "Informe Final",
        "Informe de Avance",
    }
)


def puntaje_texto_para_word(raw: Any) -> str | None:
    """Texto para línea «Puntaje: …» del Word (coma decimal, 2 decimales)."""
    if raw in (None, ""):
        return None
    n = parse_puntaje(raw)
    if n is None or n <= 0:
        return None
    x = float(n)
    for _ in range(10):
        if x <= 1000:
            break
        if abs(x - round(x)) >= 1e-4:
            break
        ri = int(round(x))
        if ri % 100 != 0:
            break
        x = x / 100.0
    if x <= 0 or x > 1000:
        return None
    return f"{x:.2f}".replace(".", ",")


def _formato_monto(monto: Any) -> str:
    try:
        valor = int(float(monto))
        return f"${valor:,}".replace(",", ".")
    except (TypeError, ValueError):
        return str(monto or "")


def _linea_director(nombre: str, categoria: str) -> str:
    nombre = str(nombre or "").strip()
    categoria = str(categoria or "").strip()
    if not nombre and not categoria:
        return ""
    if not categoria or categoria.startswith("Seleccionar"):
        return f"   Director: {nombre}\n"
    return f"   Director: {nombre} ({categoria})\n"


def _linea_codirector(nombre: str, categoria: str) -> str:
    nombre = str(nombre or "").strip()
    categoria = str(categoria or "").strip()
    if not nombre and not categoria:
        return ""
    if not categoria or categoria.startswith("Seleccionar"):
        return f"   Codirector: {nombre}\n"
    return f"   Codirector: {nombre} ({categoria})\n"


def _agregar_tema_ci(doc: Document, contador: int, tema: dict[str, Any]) -> int:
    inv = tema.get("investigacion") or {}
    tipo = inv.get("tipo") or tema.get("tipo_actividad", "")
    titulo = inv.get("titulo") or tema.get("actividad", "")
    descripcion = inv.get("descripcion") or tema.get("detalle", "")

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1

    run = p.add_run(f"{contador}. {tipo} - {titulo}\n")
    run.bold = True
    run.font.color.rgb = VERDE

    if descripcion:
        p.add_run(f"   Descripción: {descripcion}\n")

    if tipo == "Categorización Docente":
        if inv.get("apellido_nombre_docente"):
            p.add_run(f"   Docente: {inv['apellido_nombre_docente']}\n")
        if inv.get("dni_docente"):
            p.add_run(f"   DNI: {inv['dni_docente']}\n")
    elif tipo in TIPOS_CON_DIRECTOR:
        linea = _linea_director(inv.get("director", ""), inv.get("cat_director", ""))
        if linea:
            p.add_run(linea)
        linea = _linea_codirector(inv.get("codirector", ""), inv.get("cat_codirector", ""))
        if linea:
            p.add_run(linea)

    equipo = str(inv.get("equipo") or "").strip()
    if equipo:
        p.add_run(f"   Equipo: {equipo.replace(chr(10), '; ')}\n")

    p.add_run(f"   Unidad Académica: {tema.get('unidad_academica', '—')}\n")

    txt_puntaje = puntaje_texto_para_word(inv.get("puntaje"))
    if txt_puntaje:
        p.add_run(f"   Puntaje: {txt_puntaje}\n")

    if inv.get("resolucion_cd"):
        p.add_run(f"   Resolución CD: {inv['resolucion_cd']}\n")
    if inv.get("resolucion_cs"):
        p.add_run(f"   Resolución CS del Proyecto: {inv['resolucion_cs']}\n")
    if inv.get("instituto"):
        p.add_run(f"   Instituto: {inv['instituto']}\n")
    if inv.get("catedra"):
        p.add_run(f"   Cátedra: {inv['catedra']}\n")
    if inv.get("tipo_financiamiento"):
        p.add_run(f"   Financiamiento: {inv['tipo_financiamiento']}\n")
    if inv.get("fuente_financiamiento"):
        p.add_run(f"   Fuente: {inv['fuente_financiamiento']}\n")
    if inv.get("responsable_de_carga"):
        p.add_run(f"   Responsable de carga: {inv['responsable_de_carga']}\n")
    if inv.get("monto_financiamiento"):
        p.add_run(f"   Monto: {_formato_monto(inv['monto_financiamiento'])}\n")
    if inv.get("alumnos"):
        p.add_run(f"   Alumnos: {inv['alumnos']}\n")

    return contador + 1


def generar_orden_del_dia(
    temas: list[dict[str, Any]],
    unidad: str,
    sede: str,
    anio: str,
    fecha_reunion: str | None = None,
    organo: str = "Consejo Directivo",
) -> bytes:
    doc = Document()

    section = doc.sections[0]
    section.top_margin = Cm(1.5)
    section.bottom_margin = Cm(1.5)
    section.left_margin = Cm(2)
    section.right_margin = Cm(2)

    table = doc.add_table(rows=1, cols=2)
    table.autofit = True
    cell_logo, cell_text = table.rows[0].cells

    if LOGO.exists():
        cell_logo.paragraphs[0].add_run().add_picture(str(LOGO), width=Cm(2.2))

    p = cell_text.paragraphs[0]
    run = p.add_run("Universidad Católica de Cuyo")
    run.bold = True
    run.font.size = Pt(14)
    run.font.color.rgb = VERDE
    p2 = cell_text.add_paragraph()
    r2 = p2.add_run("LUMEN — Orden del Día Institucional")
    r2.font.size = Pt(11)
    r2.font.color.rgb = ROJO

    doc.add_paragraph("")

    titulo = doc.add_paragraph()
    titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rt = titulo.add_run("ORDEN DEL DÍA")
    rt.bold = True
    rt.font.size = Pt(16)
    rt.font.color.rgb = VERDE

    subt = doc.add_paragraph()
    subt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rs = subt.add_run(organo)
    rs.bold = True
    rs.font.size = Pt(12)
    rs.font.color.rgb = ROJO

    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta.add_run(f"{unidad}\n").bold = True
    meta.add_run(f"Sede: {sede}  ·  Año: {anio}\n")
    if fecha_reunion:
        meta.add_run(f"Fecha de reunión: {fecha_reunion}\n")
    elif temas:
        fechas = sorted({t.get("fecha_reunion") for t in temas if t.get("fecha_reunion")})
        if len(fechas) == 1:
            meta.add_run(f"Fecha de reunión: {fechas[0]}\n")
    meta.add_run(f"Generado: {datetime.now():%d/%m/%Y %H:%M}")

    doc.add_paragraph("")
    intro = doc.add_paragraph()
    if organo == "Consejo Superior":
        texto = (
            "Temas para tratamiento en Consejo Superior. "
            "Incluye propuestas elevadas por unidades académicas y cargadas por Rectorado / SGA."
        )
    else:
        texto = f"Temas propuestos para tratamiento en {organo}."
    intro.add_run(texto + " Prototipo LUMEN (no impacta planillas productivas).").italic = True

    doc.add_paragraph("")

    if not temas:
        doc.add_paragraph("No hay temas cargados para los filtros seleccionados.")
    elif organo == "Consejo de Investigación":
        contador = 1
        unidad_actual = ""
        for tema in temas:
            unidad = tema.get("unidad_academica", "—")
            if unidad != unidad_actual:
                doc.add_paragraph("")
                h = doc.add_paragraph()
                run_h = h.add_run(unidad)
                run_h.bold = True
                run_h.font.size = Pt(12)
                run_h.font.color.rgb = RGBColor(0, 102, 204)
                unidad_actual = unidad
            contador = _agregar_tema_ci(doc, contador, tema)
    else:
        for i, tema in enumerate(temas, start=1):
            head = doc.add_paragraph()
            rh = head.add_run(f"{i}. {tema.get('actividad', '(sin título)')}")
            rh.bold = True
            rh.font.size = Pt(11)
            rh.font.color.rgb = VERDE

            lines = [
                f"Unidad: {tema.get('unidad_academica', '—')}",
                f"Sesión: {tema.get('fecha_reunion', '—')}",
                f"Tipo: {tema.get('tipo_actividad', '—')}",
                f"Ámbito: {tema.get('ambito', '—')}",
            ]
            if tema.get("elevado_desde_cd"):
                lines.append(f"Elevado desde CD: {tema.get('fecha_cd', '—')}")
            if tema.get("impacta_pei"):
                lines.append(f"Objetivo PEI: {tema.get('objetivo_especifico', '—')}")
            else:
                lines.append("Impacta PEI: No")
            if tema.get("detalle"):
                lines.append(f"Detalle: {tema['detalle']}")
            lines.append(f"ID: {tema.get('id', '—')}")

            for line in lines:
                p = doc.add_paragraph(line)
                p.paragraph_format.left_indent = Cm(0.5)
                p.paragraph_format.space_after = Pt(2)

            doc.add_paragraph("")

    pie = doc.add_paragraph()
    pie.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rp = pie.add_run("UCCuyo · Testimonium de Lumine · Prototipo LUMEN")
    rp.font.size = Pt(9)
    rp.font.color.rgb = VERDE

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


def nombre_archivo_od(
    organo: str,
    unidad: str,
    anio: str,
    fecha_reunion: str | None = None,
    fecha_iso: str | None = None,
) -> str:
    prefijos = {
        "Consejo Superior": "CS",
        "Consejo de Investigación": "CI",
        "Consejo de Extensión": "CE",
        "Consejo Directivo": "CD",
    }
    prefijo = prefijos.get(organo, "OD")
    slug_ua = _slug(unidad) if unidad != "Todas las unidades" else "Institucional"
    if fecha_iso:
        slug_fecha = fecha_iso.replace("-", "")
    elif fecha_reunion:
        slug_fecha = _slug(fecha_reunion)[:24]
    else:
        slug_fecha = anio
    return f"LUMEN_OD_{prefijo}_{slug_ua}_{slug_fecha}.docx"
