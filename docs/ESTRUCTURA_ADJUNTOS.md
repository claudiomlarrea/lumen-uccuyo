# Estructura de carpetas — adjuntos LUMEN (institucional)

Propuesta para almacenar documentos ligados a temas de consejos **sin usar Drive personal** (ni de la SGA ni de una UA). El dueño es una **cuenta institucional / de servicio** de LUMEN–UCCuyo.

El adjunto es **opcional**: muchos temas son solo información y no llevan archivo.

---

## Principios

1. **Un tema = un `tema_id` estable.** El archivo viaja con ese id al elevar a CS (no se vuelve a subir).
2. **Dueño institucional.** Carpeta raíz propiedad de `lumen@…` o cuenta de servicio; personas solo tienen acceso de lectura/escritura según rol.
3. **Separar por año académico/calendario** para archivar y depurar.
4. **Ruta predecible** para que la app (y TI) ubique el archivo sin carpetas sueltas.
5. **Misma lógica que CI**, pero unificada para CD, CI, CE y CS.

---

## Raíz propuesta (Google Drive o equivalente)

```
LUMEN-UCCuyo/                          ← raíz institucional (propiedad cuenta LUMEN)
└── Adjuntos/
    └── {AAAA}/                        ← año (ej. 2026)
        ├── 01_Unidades/               ← carga y tratamiento en consejo de unidad
        ├── 02_Consejo_Superior/       ← sesión CS (cronograma institucional)
        └── 99_Archivo/                ← opcional: temas cerrados / años anteriores
```

Equivalentes en otros sistemas:

| Sistema | Raíz equivalente |
|---------|------------------|
| Google Drive | Unidad compartida `LUMEN-UCCuyo` → `Adjuntos` |
| Google Cloud Storage | bucket `lumen-uccuyo-adjuntos` → prefijos iguales |
| SharePoint | Sitio LUMEN → biblioteca `Adjuntos` → mismas carpetas |

---

## Rama 1 — Unidades académicas (CD / CI / CE)

Temas cargados y tratados en el consejo de la unidad, **antes o después** de elevar.

```
01_Unidades/
└── {Codigo_UA}/
    └── {Organo}/                      ← CD | CI | CE
        └── {YYYY-MM-DD}_reunion/      ← fecha del consejo de unidad (ISO)
            └── {tema_id}/
                ├── meta.json          ← opcional (nombre original, mime, hash, quién subió)
                └── adjunto.{ext}      ← único archivo vigente (reemplaza al anterior)
```

### Ejemplo

```
01_Unidades/
└── FCM-SJ/
    └── CD/
        └── 2026-07-22_reunion/
            └── LUM-2026-FCM-SJ-0042/
                ├── meta.json
                └── adjunto.pdf
```

### Códigos de órgano (carpetas cortas)

| Carpeta | Órgano |
|---------|--------|
| `CD` | Consejo Directivo |
| `CI` | Consejo de Investigación |
| `CE` | Consejo de Extensión |

### Códigos de UA (sugeridos)

Usar **códigos cortos estables** (no el nombre largo), para que las rutas no se rompan si cambia el rótulo en catálogo.

| Código | Unidad |
|--------|--------|
| `FCM-SJ` | Facultad de Ciencias Médicas San Juan |
| `FCM-SL` | Facultad de Ciencias Médicas San Luis |
| `FCEyE-SJ` | Facultad de Ciencias Económicas y Empresariales San Juan |
| `FCEyE-SL` | Facultad de Ciencias Económicas y Empresariales San Luis |
| `FDCS-SJ` | Facultad de Derecho y Ciencias Sociales San Juan |
| `FDCS-SL` | Facultad de Derecho y Ciencias Sociales San Luis |
| `FFYH` | Facultad de Filosofía y Humanidades |
| `FCQT` | Facultad de Ciencias Químicas y Tecnológicas |
| `FEDU` | Facultad de Educación |
| `FCV` | Facultad de Ciencias Veterinarias |
| `FDB` | Facultad Don Bosco |
| `ECRP` | Escuela de Cultura Religiosa y Pastoral |
| `ESEG` | Escuela de Seguridad |
| `IFD-SM` | Instituto de Formación Docentes Santa María |
| `IFD-SB` | Instituto de Formación Docentes San Buenaventura |
| `SGA` | Secretaría General Académica |
| `RECT` | Rectorado |
| `…` | (completar el resto del catálogo LUMEN con TI) |

La app guarda el mapeo `unidad_academica` → `Codigo_UA` en un catálogo versionado.

---

## Rama 2 — Consejo Superior (cronograma fijo)

Los miembros del CS y la SGA trabajan por **sesión institucional** (fechas del cronograma CS).

```
02_Consejo_Superior/
└── {YYYY-MM-DD}_sesion_{sede-o-modalidad}/
    └── {Codigo_UA_origen}/
        └── {tema_id}/
            ├── meta.json
            └── adjunto.{ext}          ← mismo contenido que en 01_Unidades (ver política)
```

### Ejemplo

Tema elevado desde FCM-SJ a la sesión CS del 31/07/2026 (San Juan):

```
02_Consejo_Superior/
└── 2026-07-31_sesion_San-Juan/
    └── FCM-SJ/
        └── LUM-2026-FCM-SJ-0042/
            ├── meta.json
            └── adjunto.pdf
```

Convención de nombre de sesión:

```
{YYYY-MM-DD}_sesion_{San-Juan|San-Luis|Rodeo-del-Medio|Virtual}
```

Alineado al cronograma CS 2026 ya cargado en LUMEN.

---

## Política al elevar (tema + archivo)

**Regla de producto:** al “Elevar a Consejo Superior” no se pide re-subir el archivo.

| Opción | Qué hace | Recomendación |
|--------|----------|---------------|
| **A — Copia** | Al elevar, la app copia `01_…/{tema_id}/` → `02_…/{tema_id}/` | **Recomendada** para demo y auditoría por sesión CS |
| **B — Enlace / acceso** | Un solo archivo físico; en `02_` solo un acceso o puntero (`link.json` con `ruta_origen`) | Más limpia en storage; Drive “atajos” son frágiles |
| **C — Solo metadato** | El archivo queda en `01_`; LUMEN guarda `ruta_storage` y sirve la descarga a CS/SGA | Ideal con GCS/API; Drive “manual” no alcanza |

Para **Google Drive institucional** arrancar con **opción A (copia al elevar)**.  
Si más adelante usan **GCS**, preferir **C** (una sola copia + metadata en LUMEN).

Si el tema **no tiene adjunto**, se eleva igual: no se crea carpeta de archivo (o se crea vacía solo si TI lo pide para trazabilidad).

---

## Nombre del archivo y `meta.json`

Dentro de `{tema_id}/`:

```
adjunto.{ext}     ← nombre técnico fijo (pdf, docx, xlsx, …)
meta.json         ← nombre original y trazabilidad
```

Ejemplo `meta.json`:

```json
{
  "tema_id": "LUM-2026-FCM-SJ-0042",
  "nombre_original": "Resolucion_CD_15-2026.pdf",
  "mime": "application/pdf",
  "tamano_bytes": 245760,
  "hash_sha256": "…",
  "subido_por": "usuario.institucional",
  "subido_en": "2026-07-20T14:32:00",
  "organo_origen": "Consejo Directivo",
  "unidad_codigo": "FCM-SJ",
  "elevado_cs": true,
  "sesion_cs": "2026-07-31_sesion_San-Juan",
  "viaja_con_tema": true
}
```

En LUMEN el campo del tema guarda al menos: `ruta_storage`, `nombre_original`, `tamano_bytes`.

---

## Permisos sugeridos (Drive / SharePoint)

| Rol | `01_Unidades/{su_UA}` | Otras UA en `01_` | `02_Consejo_Superior` |
|-----|------------------------|-------------------|------------------------|
| Secretario/a de UA | Lectura + escritura | Sin acceso (o solo lectura si TI lo define) | Lectura de lo elevado por su UA |
| Miembros consejo de unidad | Lectura | — | — |
| Secretaría General Académica | Lectura (todas) | Lectura | Lectura + organizar / devolver |
| Miembros Consejo Superior | — | — | Lectura (todas las sesiones) |
| Cuenta servicio LUMEN | Total (API) | Total | Total |
| Personas (Drive personal) | **Ninguno como dueños** | — | — |

La descarga cotidiana debería hacerse **desde LUMEN** (botón Descargar); Drive es el depósito, no el flujo de trabajo.

---

## Vista mental del flujo

```text
[UA carga tema ± archivo]
        ↓
  01_Unidades / UA / CD|CI|CE / fecha / tema_id /
        ↓  miembros UA: descargar · leer · aprobar
        ↓
  [Elevar a CS]  →  copia (o puntero) a
        ↓
  02_Consejo_Superior / sesión_CS / UA / tema_id /
        ↓  SGA revisa · CS descarga y analiza
```

Sin adjunto: solo se mueve el **registro del tema** en LUMEN; no hay carpeta de archivo.

---

## Qué pedir a TI (checklist)

1. Crear unidad compartida / sitio **`LUMEN-UCCuyo`** (no cuenta personal).
2. Crear raíz `Adjuntos/{año}/01_Unidades` y `02_Consejo_Superior`.
3. Pre-crear carpetas por `Codigo_UA` (o permitir que la cuenta de servicio las cree).
4. Cuenta de servicio con permiso de escritura; compartir IDs de carpeta raíz con LUMEN (secrets).
5. Definir retención: p. ej. mover años cerrados a `99_Archivo` a los 2 años.
6. Cuota y tipos permitidos: PDF, Word, Excel, PowerPoint, imágenes; tope p. ej. 10–25 MB por archivo.

---

## Relación con el prototipo actual

Hoy LUMEN guarda en disco local / sesión:

```
data/store/adjuntos/{tema_id}/
```

Eso es **temporal** (demo). La estructura de este documento es el **destino institucional** cuando se active Drive/GCS: mismo `tema_id`, misma idea de “viaja con el tema”, rutas estables por año / UA / órgano / sesión CS.
