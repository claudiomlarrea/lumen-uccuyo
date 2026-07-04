# Integración LUMEN → Google Sheets

Programada y **desactivada por defecto**. El prototipo simula filas sin escribir en planillas productivas.

## Destinos

| Destino | Sheet | Tablero |
|---|---|---|
| Formulario Único PEI | [1c-ZPobdyqA5pW9mhyJsC1uJwFFAcEv4HliOjcSwhOsg](https://docs.google.com/spreadsheets/d/1c-ZPobdyqA5pW9mhyJsC1uJwFFAcEv4HliOjcSwhOsg/edit#gid=511573903) | [Looker PEI](https://datastudio.google.com/u/1/reporting/1402e4de-9e87-4543-b7f3-4ba714819429/page/p_2mexfiotmd) |
| Datos Consejo Investigación | [17MiyW17W7oLIwSCKjDXCoA85CwBkYqHYhDKblVN37c8](https://docs.google.com/spreadsheets/d/17MiyW17W7oLIwSCKjDXCoA85CwBkYqHYhDKblVN37c8/edit#gid=1058037844) | [Looker Investigación](https://datastudio.google.com/u/1/reporting/42923975-d3ff-4972-acd7-ab51db384f13/page/p_xtiikpfv2d) |

## Reglas

1. **Toda actividad con `impacta_pei = true`** y estado aprobado → fila en **Formulario Único PEI**.
2. **Temas de investigación** (`es_investigacion = true`) → fila en **Datos Consejo de Investigación**.
3. **Investigación + PEI** → **ambas** planillas (como hoy en los dos sistemas separados).

## Código

- `services/integracion/config.py` — IDs, URLs, flag `habilitada`
- `services/integracion/mapeo_pei.py` — tema → columnas PEI (OG 1–6)
- `services/integracion/mapeo_investigacion.py` — tema → columnas Hoja 2 CI
- `services/integracion/publicador.py` — orquestación
- `services/integracion/sheets_client.py` — gspread (solo si `habilitada = true`)

## UI

Pantalla **Simulación PEI** — preview CSV + botón “Ejecutar simulación de publicación” (dry-run).

## Activar escritura real (futuro)

1. `pip install -r requirements-integracion.txt`
2. Secrets: ver `.streamlit/secrets.toml.example`
3. Compartir ambas planillas con el service account
4. `[lumen_integracion] habilitada = true`

## Campos de investigación extendidos

El bloque opcional `investigacion` en cada tema (director, puntaje, financiamiento, etc.) se mapeará al cargar el formulario ampliado de CI. Hasta entonces, LUMEN usa los campos genéricos (`actividad`, `detalle`, `tipo_actividad`).
