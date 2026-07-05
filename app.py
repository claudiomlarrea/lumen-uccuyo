"""
LUMEN — Orden del Día Institucional y vinculación al PEI
Prototipo de demostración (no escribe en Google Sheets productivos).
"""

import streamlit as st

from ui import hero_logo, setup_page, sidebar_brand

setup_page("LUMEN · UCCuyo")
sidebar_brand()

col_logo, col_text = st.columns([1, 5])
with col_logo:
    hero_logo(130)
with col_text:
    st.markdown(
        """
        <div class="lumen-hero" style="border:none;box-shadow:none;padding-left:0;background:transparent;">
          <div>
            <div class="lumen-badge">PROTOTIPO · UCCUYO</div>
            <h1>LUMEN</h1>
            <p>Orden del Día Institucional y vinculación al Plan Estratégico Institucional (PEI)</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="lumen-note">
    <strong>Modo seguro:</strong> este sistema es independiente. No interfiere con el cargador de temas
    del Consejo de Investigación ni escribe en Google Sheets del PEI o de Investigación.
    Todo se guarda en archivos locales del prototipo para que puedas probar el flujo completo.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### ¿Qué es LUMEN?")
st.write(
    """
    **LUMEN** (del lema institucional *Testimonium de Lumine*) es el prototipo de un sistema único
    para que todas las unidades académicas y administrativas carguen temas al **orden del día**
    de sus consejos, con la mayor cantidad de campos en desplegables, y visualicen cómo esas
    actividades se vincularían automáticamente a los **objetivos específicos del PEI**.
    """
)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        """
        <div class="lumen-card">
        <h4>1. Cargar temas</h4>
        <div class="lumen-meta">Desplegables de UA, tipo, actividad y objetivo PEI.
        Opción de carga manual si no está en el catálogo.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        """
        <div class="lumen-card">
        <h4>2. Orden del día</h4>
        <div class="lumen-meta">Cada UA descarga su Word (CD/CI/CE) por fecha.
        Todos descargan el OD del Consejo Superior por sesión.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        """
        <div class="lumen-card">
        <h4>3. Simulación PEI</h4>
        <div class="lumen-meta">Vista previa de lo que impactaría en el Tablero PEI,
        sin publicar en producción.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### Cómo probarlo")
st.markdown(
    """
1. Andá a **Cargar temas** y registrá actividades de distintas UA (podés adjuntar un documento opcional).  
2. Si no adjuntaste al cargar, usá **Carga de archivos** (como en Consejo de Investigación).  
3. Revisá el **Orden del día** y descargá el Word.  
4. Marcá temas como aprobados y mirá la **Simulación PEI**.  
5. En **Catálogos** ves cómo crecen las opciones cargadas a mano.
"""
)

st.markdown(
    """
    <div class="lumen-footer">
    Universidad Católica de Cuyo · Testimonium de Lumine · Manual de Marcas UCCuyo<br/>
    LUMEN — prototipo de demostración para Secretaría de Investigación / PEI institucional
    </div>
    """,
    unsafe_allow_html=True,
)
