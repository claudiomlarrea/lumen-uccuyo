"""Actividades habituales extraídas de Órdenes del Día del Consejo Superior.

Fuente: actas CS 946, 947, 951, 953, 955, 956, 957, 958 (2025) y 959, 961 (2026).
Son denominaciones cortas recurrentes que las UA elevan desde CD/CI/CE al CS.
"""

from __future__ import annotations

TIPOS_HABITUALES_CS = [
    "Designación docente",
    "Renuncia docente",
    "Licencia docente",
    "Creación de Carrera",
    "Creación de Plan de Estudios",
    "Modificación de Plan de Estudios",
]

# PEI sugerido para tipos habituales de CS
TIPO_CS_A_OBJETIVO = {
    "Designación docente": "4.4. Implementar un Régimen de dedicación docente para  la incorporación, permanencia y promoción de los recursos humanos de la institución",
    "Renuncia docente": "4.1. Realizar el análisis de necesidades de recursos humanos de la institución",
    "Licencia docente": "4.1. Realizar el análisis de necesidades de recursos humanos de la institución",
    "Creación de Carrera": "1.6 Establecer planes de mejora",
    "Creación de Plan de Estudios": "1.6 Establecer planes de mejora",
    "Modificación de Plan de Estudios": "1.6 Establecer planes de mejora",
}

# Actividades habituales por unidad (denominaciones cortas para carga en LUMEN)
ACTIVIDADES_HABITUALES_POR_UA: dict[str, list[str]] = {
    "Secretaría General Académica": [
        "Renuncia docente Orientación Universitaria",
        "Designación docente Orientación Universitaria",
        "Designación / licencia Jefatura DEPCU",
        "Designaciones organismos dependientes de Rectorado",
        "Cuerpos de Bandera sede San Juan",
        "Cuerpos de Bandera sede San Luis",
        "Distinciones Actos de colación",
        "Calendario Académico",
        "Normas de procedimiento",
        "Ratificación de resolución de Rectorado",
    ],
    "Secretaría Investigación": [
        "Presentación de proyectos de investigación",
        "Informes finales de proyectos",
        "Informes finales PRONIS",
        "Categorización extraordinaria",
        "Convocatoria / cierre PRONIS",
        "Becas cofinanciadas CONICET",
        "Líneas prioritarias de investigación",
        "Jornadas de Investigación UCCuyo",
        "Ordenanza de Investigación",
        "Programa de fortalecimiento de Institutos",
        "Baja de proyectos",
        "Charla informativa sobre normativa de investigación",
        "Premio Domingo Faustino Sarmiento de Ciencia e Innovación",
    ],
    "Secretaría de Extensión": [
        "Designaciones Consejo de Extensión",
        "Informe anual de Extensión",
        "Becas / premios Santander alumnos de grado",
    ],
    "Rectorado": [
        "Estado de avance Plan Estratégico Institucional",
        "Plan Integral de Ahorro y Uso Responsable del Agua (AURA)",
        "Plan de Permanencia y Retención — Educación a Distancia",
        "Régimen disciplinario / ordenanza institucional",
        "Políticas de Comunicación Institucional",
        "Observatorio de Inteligencia Artificial",
        "Creación del Consejo del Observatorio de IA",
        "Comisión / referentes de Evaluación Institucional",
        "Comisión Técnica SACAU-UCCuyo",
        "Definición valor CRE (Crédito de Referencia del Estudiante)",
        "Régimen de licencias por razones particulares",
        "Actos de colación sede San Juan",
        "Día del Graduado de la UCCuyo",
    ],
    "Vicerrector/a": [
        "Títulos",
    ],
    "Vicerrector/a de Sede": [
        "Títulos",
        "Informe Congreso Internacional Ex Corde Ecclesiae",
    ],
    "Facultad de Filosofía y Humanidades": [
        "Renuncias docentes",
        "Licencias docentes",
        "Designaciones docentes y de cargos",
        "Designaciones de ayudantes alumnos",
        "Diplomatura en Inspección de Control de Calidad en Proyectos de Infraestructura",
    ],
    "Facultad de Ciencias Químicas y Tecnológicas": [
        "Renuncias docentes",
        "Licencias docentes",
        "Designaciones docentes y de cargos",
        "Designaciones miembros de comisiones",
        "Curso de ingreso — designaciones docentes",
        "Proyecto Vino de la Facultad / UCCuyo",
        "Modificación de plan de estudio — Especialización en Química Clínica",
        "Aval científico-académico a proyecto institucional",
        "Nueva carrera / CCC Licenciatura en Enología (a distancia)",
    ],
    "Facultad de Educación": [
        "Renuncias docentes / de cargos",
        "Licencias docentes",
        "Designaciones docentes y de cargos",
        "Diplomatura Superior en Apoyo a la Inclusión",
        "Diplomatura Superior Universitaria en Evaluación Neurocognitiva",
        "Diplomatura en Mediación Escolar (con Derecho)",
        "Designaciones curso de ingreso — Psicopedagogía / Psicomotricidad",
        "Modificación / rectificación de plan de estudios de carrera",
        "Acto de colación virtual — carreras a distancia",
        "Formación dirigida a empresas / articulación externa",
    ],
    "Facultad de Ciencias Médicas San Juan": [
        "Renuncias docentes",
        "Licencias docentes",
        "Designaciones docentes",
        "Designaciones de cargos",
        "Informe CAEM — Congreso Argentino de Educación Médica",
        "Creación de carrera / plan de estudios — Tecnicatura en Cuidados Domiciliarios",
        "Modificación del plan de estudio — Licenciatura en Nutrición",
    ],
    "Facultad de Ciencias Médicas San Luis": [
        "Renuncias docentes",
        "Licencias docentes",
        "Designaciones docentes",
        "Designaciones de cargos",
        "Designaciones de ayudantes alumnos",
        "Plan de estudios CCC Licenciatura en Instrumentación",
    ],
    "Facultad de Ciencias Económicas y Empresariales San Juan": [
        "Renuncias docentes / de cargos",
        "Designaciones docentes",
        "Designaciones de cargos",
        "Diplomatura en Administración Financiera del Estado",
        "Diplomatura en Gestión de Abastecimiento Minero",
        "Curso de Educación Financiera para todos",
        "Informe apertura carrera Licenciatura en Administración",
        "Aval académico-institucional — Seminario de Federalismo Fiscal",
    ],
    "Facultad de Ciencias Económicas y Empresariales San Luis": [
        "Renuncias de cargos y docentes",
        "Designaciones docentes",
        "Informe articulación con colegios de nivel medio",
    ],
    "Facultad de Derecho y Ciencias Sociales San Juan": [
        "Renuncias docentes",
        "Designaciones docentes",
        "Designaciones de cargos",
        "Diplomatura en Mediación Escolar (con Educación)",
        "Seminario Internacional de Derecho Privado",
        "Prórroga de plazo de caducidad de resolución CS",
        "Creación del Instituto de Investigación de Análisis Económico del Derecho",
    ],
    "Facultad de Derecho y Ciencias Sociales San Luis": [
        "Renuncias docentes",
        "Licencias docentes",
        "Designaciones docentes",
        "Designaciones de cargos",
        "Plan de estudios — Especialización en Derecho Público comparado",
        "Carrera / plan — Especialización en Derecho Procesal Civil y Comercial",
        "Convenio con Poder Judicial — Red de Contención Familiar",
        "Informe Programa Red de Contención Familiar",
    ],
    "Facultad de Ciencias Veterinarias": [
        "Renuncia / designaciones de cargos",
        "Designaciones docentes",
        "Creación del Instituto Equino Deportivo",
    ],
    "Facultad Don Bosco": [
        "Renuncia de secretaria académica",
        "Designaciones docentes",
        "Designaciones de cargos",
        "Ciclo de Complementación Curricular Licenciatura en Enología (presencial)",
        "Ciclo de Complementación Curricular Licenciatura en Enología (a distancia)",
        "Diplomatura en Enología",
        "Aniversario institucional de la Facultad",
    ],
    "Escuela de Seguridad": [
        "Renuncias docentes",
        "Licencias de cargo y docentes",
        "Designaciones docentes",
        "Designaciones de cargos",
        "Creación del Instituto de Seguridad y Criminalística (ISCRI)",
    ],
    "Escuela de Cultura Religiosa y Pastoral": [
        "Renuncias docentes",
        "Licencias docentes",
        "Designaciones docentes y de cargos",
        "Modalidad de dictado de materias formativas",
        "Coloquio Jesucristo Hijo de Dios Salvador",
        "Informe Jubileo Universitario y de los Educadores",
        "Calendario de cuaresma / retiro docente",
        "Curso de Formación a partir del Sínodo",
        "Designación Director de Escuela",
    ],
    "Observatorio de Inteligencia Artificial": [
        "Participación en Global ChatGPT Student Survey",
        "Creación del Consejo del Observatorio de IA",
        "Curso de Capacitación en IA para Graduados UCCuyo",
    ],
    "Departamento de Educación a Distancia": [
        "Programa de Capacitación DEaD",
        "Designación Consejo EaD",
        "Reglamento de Educación a Distancia UCCuyo",
        "Plan de Permanencia y Retención — EaD",
    ],
    "Instituto de Formación Docentes Santa María": [
        "Designaciones / asuntos de colegios e institutos",
    ],
    "Instituto de Formación Docentes San Buenaventura": [
        "Designaciones / asuntos de colegios e institutos",
    ],
}


def actividades_habituales_ua(ua: str) -> list[str]:
    return list(ACTIVIDADES_HABITUALES_POR_UA.get(ua, []))
