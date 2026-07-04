"""Catálogos institucionales del prototipo LUMEN (solo lectura local)."""

from __future__ import annotations

UNIDADES_ACADEMICAS = [
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
    "Secretaría General Académica",
    "Rectorado",
    "Vicerrector/a",
    "Vicerrector/a de Formación",
    "Vicerrector/a de Sede",
    "Consejo Superior",
    "Secretaría Académica",
    "Secretaría de Extensión",
    "Secretaría Investigación",
    "Observatorio de Inteligencia Artificial",
    "Departamento de Evaluación y Acreditación",
    "Departamento de Educación a Distancia",
    "Departamento de Graduados",
    "Coordinación General de carreras a distancia",
    "Jefatura de Sistemas",
    "Directorio",
    "Área de Orientación Universitaria",
]

SEDES = [
    "San Juan",
    "San Luis",
    "Rodeo del Medio",
    "Inter-sede",
]

ANIOS = ["2023", "2024", "2025", "2026", "2027"]

AMBITOS = [
    "Gestión institucional",
    "Docencia",
    "Investigación",
    "Extensión y vinculación",
    "Educación a distancia",
    "Estudiantes y graduados",
    "Pastoral e identidad",
]

TIPOS_ACTIVIDAD = [
    "Convenio / alianza / acta acuerdo",
    "Curso / capacitación / diplomatura",
    "Jornada / evento académico",
    "Encuentro / congreso científico",
    "Seminario / taller",
    "Charla / conferencia",
    "Plan / programa institucional",
    "Publicación / difusión",
    "Participación estudiantil",
    "Reunión institucional",
    "Extensión / vinculación",
    "Educación a distancia",
    "Evaluación / seguimiento / monitoreo",
    "Autoevaluación / acreditación / calidad",
    "Becas",
    "Graduados",
    "Celebración / evento religioso",
    "Categorización docente / investigadores",
    "Informe final",
    "Informe de avance",
    "Proyecto de investigación",
    "Proyecto de cátedra",
    "Semillero de investigación",
    "Líneas prioritarias de investigación",
    "Cronograma / planificación",
    "Normativa / reglamento",
    "Infraestructura / tecnología",
    "Emprendedurismo",
    "Responsabilidad social universitaria",
    "Comunicación institucional",
    "Otro (cargar a mano)",
]

# Tipos finos de investigación (subconjunto / refuerzo)
TIPOS_INVESTIGACION = [
    "Informe final",
    "Informe de avance",
    "Proyecto de investigación",
    "Proyecto de cátedra",
    "Jornada / evento académico",
    "Categorización docente / investigadores",
    "Líneas prioritarias de investigación",
    "Cronograma / planificación",
    "Semillero de investigación",
    "Charla / conferencia",
    "Otro (cargar a mano)",
]

OBJETIVOS_ESPECIFICOS = {
    "1": [
        "1.1   Refuncionalizar el equipo de referentes de evaluación institucional",
        "1.2 Establecer criterios e indicadores de calidad",
        "1.3 Realizar procesos sistemáticos de autoevaluación",
        "1.4 Implementar mecanismos de retroalimentación",
        "1.5 Fomentar una cultura de calidad",
        "1.6 Establecer planes de mejora",
        "1.7 Monitoreo y seguimiento periódico",
        "1.8 Promover la transparencia mediante la implementación de estrategias de monitoreo y comunicación de avance de logros y desafíos enfrentados",
    ],
    "2": [
        "2.1 Actualizar e implementar convenios y alianzas estratégicas",
        "2.2. Fortalecer la participación institucional en eventos y reuniones científico académicas",
        "2.3. Desarrollar un Plan de Comunicación interna y externa con enfoque integral",
        "2.4. Fortalecer los espacios de participación institucional",
        "2.5. Implementar dispositivos de acceso a la información institucional",
        "2.6. Fomentar la Responsabilidad Social Universitaria",
        "2.7. Desarrollar programas de educación continua",
        "2.8. Generar estrategias de articulación con Instituciones de Nivel Secundario",
    ],
    "3": [
        "3.1 Evaluar el Sistema Institucional de Educación a Distancia vigente",
        "3.2. Revisión y definición de los objetivos del SIED para la consolidación del sistema de EaD",
        "3.3. Revisión y adecuación de políticas y normativas del sistema de EaD",
        "3.4. Diseñar y desarrollar recursos educativos para la EaD",
        "3.5. Capacitación del personal docente",
        "3.6. Actualizar y adecuar la infraestructura tecnológica",
        "3.7. Implementar estrategias de apoyo y servicios a los estudiantes",
        "3.8. Promover y difundir el Sistema Institucional de Educación a Distancia para atraer nuevos estudiantes.",
        "3.9. Colaboración y alianzas estratégicas",
    ],
    "4": [
        "4.1. Realizar el análisis de necesidades de recursos humanos de la institución",
        "4.2. Comunicar y difundir la política institucional de jerarquización y permanencia de los recursos humanos de la institución",
        "4.3. Definir criterios y objetivos de jerarquización de los recursos humanos",
        "4.4. Implementar un Régimen de dedicación docente para  la incorporación, permanencia y promoción de los recursos humanos de la institución",
        "4.5. Diseñar e implementar programas de formación y capacitación permanente",
        "4.6. Desarrollar sistemas de evaluación de desempeño por competencias",
        "4.7. Realizar Revisiones periódicas y sistemáticas de las acciones implementadas.",
    ],
    "5": [
        "5.1. Facilitar la creación de espacios de participación y representación de asociaciones estudiantiles",
        "5.2. Impulsar la conformación del Consejo de Graduados y fortalecer su accionar e impacto en la Comunidad Universitaria.",
        "5.3. Promover la participación de estudiantes y graduados en actividades culturales, sociales, deportivas y recreativas, articulando con las diferentes Unidades Académicas, Secretaría de Extensión e Investigación",
        "5.4. Impulsar la participación de estudiantes y graduados en actividades de investigación",
        "5.6. Fomentar el emprendedurismo en estudiantes y graduados.",
        "5.7. Fortalecer el seguimiento de los graduados",
    ],
    "6": [
        "6.1. Gestionar espacios para fomentar la identidad propia de la institución",
        "6.2. Fortalecer la integración de los valores cristianos en el continuo accionar de la académica",
        "6.3 Celebraciones y eventos religiosos. Hacer de la celebración del Misterio Cristiano el centro de la vida espiritual universitaria.",
        "6.4. Interrelación y diálogo entre ciencia y fe",
        "6.5. Promoción del Compromiso Ético y Responsabilidad Social",
    ],
}

OBJETIVOS_GENERALES = {
    "1": "Objetivo 1: Sistema Integral de Aseguramiento de la Calidad",
    "2": "Objetivo 2: Integralidad, vinculación y comunicación",
    "3": "Objetivo 3: Sistema Institucional de Educación a Distancia",
    "4": "Objetivo 4: Jerarquización y permanencia de recursos humanos",
    "5": "Objetivo 5: Participación estudiantil y de egresados",
    "6": "Objetivo 6: Identidad cristiana, humanística y transformadora",
}

# Matriz tipo → objetivo PEI sugerido (prototipo)
TIPO_A_OBJETIVO = {
    "Convenio / alianza / acta acuerdo": "2.1 Actualizar e implementar convenios y alianzas estratégicas",
    "Curso / capacitación / diplomatura": "2.7. Desarrollar programas de educación continua",
    "Jornada / evento académico": "2.2. Fortalecer la participación institucional en eventos y reuniones científico académicas",
    "Encuentro / congreso científico": "2.2. Fortalecer la participación institucional en eventos y reuniones científico académicas",
    "Seminario / taller": "2.7. Desarrollar programas de educación continua",
    "Charla / conferencia": "6.1. Gestionar espacios para fomentar la identidad propia de la institución",
    "Plan / programa institucional": "1.6 Establecer planes de mejora",
    "Publicación / difusión": "5.4. Impulsar la participación de estudiantes y graduados en actividades de investigación",
    "Participación estudiantil": "5.3. Promover la participación de estudiantes y graduados en actividades culturales, sociales, deportivas y recreativas, articulando con las diferentes Unidades Académicas, Secretaría de Extensión e Investigación",
    "Reunión institucional": "2.4. Fortalecer los espacios de participación institucional",
    "Extensión / vinculación": "2.6. Fomentar la Responsabilidad Social Universitaria",
    "Educación a distancia": "3.5. Capacitación del personal docente",
    "Evaluación / seguimiento / monitoreo": "1.7 Monitoreo y seguimiento periódico",
    "Autoevaluación / acreditación / calidad": "1.5 Fomentar una cultura de calidad",
    "Becas": "5.4. Impulsar la participación de estudiantes y graduados en actividades de investigación",
    "Graduados": "5.2. Impulsar la conformación del Consejo de Graduados y fortalecer su accionar e impacto en la Comunidad Universitaria.",
    "Celebración / evento religioso": "6.3 Celebraciones y eventos religiosos. Hacer de la celebración del Misterio Cristiano el centro de la vida espiritual universitaria.",
    "Categorización docente / investigadores": "4.3. Definir criterios y objetivos de jerarquización de los recursos humanos",
    "Informe final": "1.7 Monitoreo y seguimiento periódico",
    "Informe de avance": "1.7 Monitoreo y seguimiento periódico",
    "Proyecto de investigación": "5.4. Impulsar la participación de estudiantes y graduados en actividades de investigación",
    "Proyecto de cátedra": "5.4. Impulsar la participación de estudiantes y graduados en actividades de investigación",
    "Semillero de investigación": "5.4. Impulsar la participación de estudiantes y graduados en actividades de investigación",
    "Líneas prioritarias de investigación": "1.4 Implementar mecanismos de retroalimentación",
    "Cronograma / planificación": "1.5 Fomentar una cultura de calidad",
    "Normativa / reglamento": "1.5 Fomentar una cultura de calidad",
    "Infraestructura / tecnología": "3.6. Actualizar y adecuar la infraestructura tecnológica",
    "Emprendedurismo": "5.6. Fomentar el emprendedurismo en estudiantes y graduados.",
    "Responsabilidad social universitaria": "2.6. Fomentar la Responsabilidad Social Universitaria",
    "Comunicación institucional": "2.3. Desarrollar un Plan de Comunicación interna y externa con enfoque integral",
}

ESTADOS = [
    "borrador",
    "en_orden_del_dia",
    "aprobado_cd",
    "pendiente_revision_sga",
    "en_orden_del_dia_cs",
    "elevado_cs",
    "aprobado_cs",
    "publicado_simulado",
]

# Unidades que cargan temas directamente al orden del día del Consejo Superior
UNIDADES_CARGA_CS_DIRECTA = {
    "Secretaría General Académica",
    "Rectorado",
    "Vicerrector/a",
    "Vicerrector/a de Formación",
    "Vicerrector/a de Sede",
    "Consejo Superior",
}

ETIQUETAS_ESTADO = {
    "borrador": "Borrador",
    "en_orden_del_dia": "En orden del día (CD)",
    "aprobado_cd": "Aprobado en CD",
    "pendiente_revision_sga": "Pendiente revisión SGA",
    "en_orden_del_dia_cs": "En orden del día CS",
    "elevado_cs": "Elevado a CS (legacy)",
    "aprobado_cs": "Aprobado en CS",
    "publicado_simulado": "Publicado (simulado)",
}


def puede_cargar_cs_directo(ua: str) -> bool:
    return ua in UNIDADES_CARGA_CS_DIRECTA


def es_unidad_academica_facultad(ua: str) -> bool:
    """Facultades, escuelas e institutos — flujo CD → elevación CS."""
    return ua not in UNIDADES_CARGA_CS_DIRECTA and ua not in {
        "Secretaría Investigación",
        "Secretaría de Extensión",
        "Observatorio de Inteligencia Artificial",
        "Departamento de Evaluación y Acreditación",
        "Departamento de Educación a Distancia",
        "Departamento de Graduados",
        "Coordinación General de carreras a distancia",
        "Jefatura de Sistemas",
        "Directorio",
        "Área de Orientación Universitaria",
        "Secretaría Académica",
    }

# Actividades de ejemplo por UA (semilla del prototipo; se amplían con cargas manuales)
ACTIVIDADES_EJEMPLO = {
    "Secretaría Investigación": [
        "Presentación del cronograma anual",
        "Rendición de cuentas y cierre del Programa PRONIS",
        "Propuesta de categorización anual de investigadores",
        "Charla informativa sobre nueva normativa",
        "Planificación de Jornadas de Investigación",
        "Semillero de Inteligencia Artificial",
        "Programa de Fortalecimiento de los Institutos",
        "Líneas prioritarias de investigación",
    ],
    "Rectorado": [
        "Participación en reunión regional ODUCAL",
        "Presentación institucional del Plan AURA",
        "Reunión de equipos de gestión",
    ],
    "Secretaría General Académica": [
        "Informe de gestión académica",
        "Propuesta normativa académica",
        "Seguimiento de acreditaciones",
    ],
    "Facultad de Ciencias Económicas y Empresariales San Juan": [
        "Firma de convenio con municipio",
        "Diplomatura en industria minera",
        "Jornada de puertas abiertas",
    ],
}


def all_objetivos() -> list[str]:
    items: list[str] = []
    for key in sorted(OBJETIVOS_ESPECIFICOS.keys()):
        items.extend(OBJETIVOS_ESPECIFICOS[key])
    return items


def objetivo_general_de(especifico: str) -> str:
    if not especifico:
        return ""
    code = especifico.strip()[:1]
    return OBJETIVOS_GENERALES.get(code, "")


def sugerir_objetivo(tipo: str) -> str | None:
    return TIPO_A_OBJETIVO.get(tipo)
