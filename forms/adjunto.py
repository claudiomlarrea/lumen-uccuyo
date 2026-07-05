"""UI de adjuntos opcionales — patrón Consejo de Investigación adaptado a LUMEN."""

from __future__ import annotations

from typing import Any

import streamlit as st

from data.storage import actualizar_tema
from services.adjuntos import (
    EXTENSIONES_PERMITIDAS,
    MAX_BYTES,
    eliminar_adjunto,
    guardar_adjunto,
    leer_adjunto,
    meta_adjunto,
    tiene_adjunto,
    validar_archivo,
)


def _caption_ci() -> None:
    st.caption(
        "Como en el **Consejo de Investigación**: el documento (resolución, informe, proyecto, etc.) "
        "es **opcional** al cargar el tema. Podés subirlo ahora o después en **Carga de archivos**."
    )


def render_uploader_adjunto(*, key: str = "adj") -> Any:
    """Uploader opcional para el formulario de carga de temas."""
    st.subheader("Documento adjunto (opcional)")
    _caption_ci()
    return st.file_uploader(
        "Seleccionar archivo",
        type=list(EXTENSIONES_PERMITIDAS),
        key=f"{key}_file",
        help=f"Máx. {MAX_BYTES // (1024 * 1024)} MB · PDF, Word, Excel, PowerPoint o imagen",
    )


def procesar_adjunto_al_guardar(tema_id: str, uploaded_file: Any) -> bool:
    """Guarda adjunto y actualiza metadata del tema. Devuelve True si se guardó."""
    if uploaded_file is None:
        return False
    errores = validar_archivo(uploaded_file)
    if errores:
        for e in errores:
            st.error(e)
        return False
    meta = guardar_adjunto(tema_id, uploaded_file)
    actualizar_tema(tema_id, {"adjunto": meta})
    return True


def render_gestion_adjunto_tema(tema: dict[str, Any]) -> None:
    """Panel para subir, descargar o quitar adjunto de un tema existente."""
    tema_id = tema["id"]
    st.markdown(f"**{tema.get('actividad', tema_id)}**")
    st.caption(
        f"{tema_id} · {tema.get('unidad_academica', '—')} · "
        f"{tema.get('organo_tratamiento', '—')} · {tema.get('fecha_reunion', '—')}"
    )

    if tiene_adjunto(tema_id):
        payload = leer_adjunto(tema_id)
        meta = meta_adjunto(tema_id) or tema.get("adjunto") or {}
        if payload:
            data, meta = payload
            st.success(f"Archivo cargado: **{meta.get('nombre_original', 'adjunto')}**")
            st.download_button(
                "Descargar adjunto",
                data=data,
                file_name=meta.get("nombre_original", "adjunto"),
                mime=meta.get("mime") or "application/octet-stream",
                key=f"dl_adj_{tema_id}",
            )
        if st.button("Quitar adjunto", key=f"rm_adj_{tema_id}"):
            eliminar_adjunto(tema_id)
            actualizar_tema(tema_id, {"adjunto": None})
            st.rerun()
    else:
        st.info("Sin documento adjunto.")

    uploaded = st.file_uploader(
        "Subir o reemplazar archivo",
        type=list(EXTENSIONES_PERMITIDAS),
        key=f"up_adj_{tema_id}",
    )
    if uploaded and st.button("Guardar archivo", key=f"save_adj_{tema_id}"):
        if procesar_adjunto_al_guardar(tema_id, uploaded):
            st.success("Archivo guardado.")
            st.rerun()
