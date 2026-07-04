# LUMEN — Orden del Día Institucional (prototipo UCCuyo)

**LUMEN** (del lema institucional *Testimonium de Lumine*) es un prototipo independiente para:

1. Cargar temas al orden del día de cualquier unidad académica o administrativa.
2. Usar la mayor cantidad de campos en desplegables, con carga manual si la opción no existe.
3. Sugerir el objetivo específico del PEI según el tipo de actividad.
4. Generar y descargar el orden del día en Word.
5. Simular el impacto en PEI e Investigación **sin escribir** en Google Sheets productivos.

## Importante

Este sistema **no interfiere** con:

- el cargador de temas del Consejo de Investigación,
- el Google Sheet de Datos Consejo Investigación,
- el Formulario Único PEI,
- el Tablero PEI institucional.

Los datos del prototipo se guardan en `data/store/` (JSON).

## Ejecutar en local

```bash
cd agenda-pei-uccuyo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Desplegar en Streamlit Cloud

1. Subí este repositorio a GitHub (puede ser **privado**).
2. Entrá a [share.streamlit.io](https://share.streamlit.io) con tu cuenta de GitHub.
3. **New app** → elegí el repo → **Main file path:** `app.py`.
4. Deploy. La URL será del tipo `https://<app>.streamlit.app`.

No hace falta configuración extra: las descargas Word usan `st.download_button` estándar.

### Datos en Cloud

- `data/store/temas.json` y catálogos viajan con el repo como datos de demo.
- En Cloud, los cambios persisten mientras la app no se redeploye desde cero.
- Para producción futura convendrá conectar Google Sheets o una base de datos.

### Integración Google Sheets (programada, apagada)

Ver [docs/INTEGRACION_SHEETS.md](docs/INTEGRACION_SHEETS.md). La pantalla **Simulación PEI** muestra las filas que irían al Formulario Único PEI y al sheet de Consejo de Investigación **sin escribir** hasta activar secrets.

## Páginas

| Página | Función |
|---|---|
| Inicio | Presentación del prototipo |
| Cargar temas | Formulario con desplegables + manual |
| Orden del día | Listado, estados CD/CS y descarga Word |
| Simulación PEI | Vista previa de filas PEI / Investigación |
| Catálogos | UA, tipos, matriz PEI y opciones manuales |

## Identidad visual

Colores y logo tomados del **Manual de Marcas UCCuyo**. Logos en `assets/`.
