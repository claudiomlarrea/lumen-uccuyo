"""Simulación de impacto PEI e Investigación — integración programada, escritura desactivada."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from data.storage import actualizar_tema, load_temas
from services.integracion.config import (
    CONSEJO_FORM_URL,
    INVESTIGACION_LOOKER_URL,
    PEI_FORM_URL,
    PEI_LOOKER_URL,
    modo_actual,
)
from services.integracion.mapeo_investigacion import fila_consejo_investigacion
from services.integracion.mapeo_pei import fila_formulario_pei
from services.integracion.publicador import (
    destinos_de_tema,
    es_publicable_investigacion,
    es_publicable_pei,
    publicar_temas,
    resumen_publicacion,
)
from ui import setup_page, sidebar_brand

setup_page("Simulación PEI · LUMEN")
sidebar_brand("Simulación PEI")

modo = modo_actual()
temas = load_temas()
stats = resumen_publicacion(temas)

st.markdown("## Simulación de publicación en tableros")
st.markdown(
    """
    <div class="lumen-note">
    <strong>Modo seguro:</strong> la integración con Google Sheets está <strong>programada</strong>
    pero <strong>desactivada</strong>. LUMEN muestra las filas que se enviarían a cada planilla
    productiva; <em>no escribe</em> hasta que se habilite en secrets.
    </div>
    """,
    unsafe_allow_html=True,
)

estado_int = "🔴 DESACTIVADA (solo simulación)" if not modo.habilitada else "🟢 HABILITADA (escritura real)"
st.info(f"Integración Google Sheets: **{estado_int}**")

st.markdown("### Reglas de destino")
st.markdown(
    f"""
| Destino | Planilla | Tablero |
|---|---|---|
| **Formulario Único PEI** | [Sheet PEI]({PEI_FORM_URL}) | [Looker PEI]({PEI_LOOKER_URL}) |
| **Datos Consejo Investigación** | [Sheet CI]({CONSEJO_FORM_URL}) | [Looker Investigación]({INVESTIGACION_LOOKER_URL}) |

- **Toda actividad con impacto PEI** (aprobada CD/CS) → Formulario Único PEI.
- **Temas de investigación** (aprobados / en OD) → **ambos** destinos si además impactan PEI.
- **Solo investigación sin PEI** → solo sheet de Consejo de Investigación.
"""
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Publicables PEI", stats["publicables_pei"])
c2.metric("Publicables Investigación", stats["publicables_investigacion"])
c3.metric("Solo PEI", stats["solo_pei"])
c4.metric("PEI + Investigación", stats["pei_e_investigacion"])

publicables_pei = [t for t in temas if es_publicable_pei(t)]
publicables_inv = [t for t in temas if es_publicable_investigacion(t)]

st.markdown("### Simular envío (sin escribir en Sheets)")
if st.button("Ejecutar simulación de publicación", use_container_width=True):
    resultado = publicar_temas(temas)
    st.session_state["lumen_sim_pub"] = resultado
    st.success(
        f"Simulación: {resultado['filas_pei']} fila(s) PEI · "
        f"{resultado['filas_investigacion']} fila(s) Investigación · "
        f"{'dry-run' if resultado['dry_run'] else 'escritura real'}."
    )

if st.button("Marcar publicables como 'publicado_simulado' (estado LUMEN)", use_container_width=True):
    n = 0
    for t in publicables_pei:
        actualizar_tema(
            t["id"],
            {
                "estado": "publicado_simulado",
                "publicado_pei_simulado": True,
                "publicado_investigacion_simulado": bool(t.get("es_investigacion")),
            },
        )
        n += 1
    for t in publicables_inv:
        if not t.get("impacta_pei"):
            actualizar_tema(t["id"], {"publicado_investigacion_simulado": True})
    st.success(f"Estados locales actualizados ({n} temas PEI).")
    st.rerun()

st.markdown("### Vista previa — Formulario Único PEI")
if publicables_pei:
    filas_pei = []
    for t in publicables_pei:
        f = fila_formulario_pei(t, modo=modo)
        filas_pei.append({k: v for k, v in f.items() if not str(k).startswith("_")})
    df_pei = pd.DataFrame(filas_pei)
    st.dataframe(df_pei, use_container_width=True, hide_index=True)
    st.download_button(
        "Descargar CSV simulación PEI",
        data=df_pei.to_csv(index=False).encode("utf-8-sig"),
        file_name="LUMEN_simulacion_Formulario_PEI.csv",
        mime="text/csv",
    )
else:
    st.info("No hay temas aprobados con impacto PEI.")

st.markdown("### Vista previa — Datos Consejo de Investigación")
if publicables_inv:
    filas_inv = []
    for t in publicables_inv:
        f = fila_consejo_investigacion(t, modo=modo)
        filas_inv.append({k: v for k, v in f.items() if not str(k).startswith("_")})
    df_inv = pd.DataFrame(filas_inv)
    st.dataframe(df_inv, use_container_width=True, hide_index=True)
    st.download_button(
        "Descargar CSV simulación Investigación",
        data=df_inv.to_csv(index=False).encode("utf-8-sig"),
        file_name="LUMEN_simulacion_Consejo_Investigacion.csv",
        mime="text/csv",
    )
else:
    st.info("No hay temas de investigación publicables.")

with st.expander("Detalle por tema — destinos"):
    rows = []
    for t in temas:
        dest = destinos_de_tema(t)
        if not dest:
            continue
        rows.append(
            {
                "ID": t.get("id"),
                "Actividad": t.get("actividad"),
                "UA": t.get("unidad_academica"),
                "Investigación": "Sí" if t.get("es_investigacion") else "No",
                "Impacta PEI": "Sí" if t.get("impacta_pei") else "No",
                "Destinos": " + ".join(dest),
            }
        )
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.caption("Ningún tema cumple criterios de publicación con los filtros de estado actuales.")

with st.expander("Cómo activar la escritura real (cuando estén listos)"):
    st.markdown(
        """
1. En Streamlit Cloud → **Secrets**, agregar:
   ```toml
   [lumen_integracion]
   habilitada = true
   correo_responsable_default = "investigacion@uccuyo.edu.ar"

   [gcp_service_account]
   type = "service_account"
   project_id = "..."
   private_key_id = "..."
   private_key = "-----BEGIN PRIVATE KEY-----\\n..."
   client_email = "..."
   client_id = "..."
   ```
2. Compartir **ambas planillas** con el `client_email` del service account (Editor).
3. Instalar dependencias: `gspread`, `google-auth` (ver `requirements-integracion.txt`).
4. Redeploy. El botón de simulación pasará a escribir filas reales.

**Hasta entonces:** solo simulación local + CSV de preview.
"""
    )
