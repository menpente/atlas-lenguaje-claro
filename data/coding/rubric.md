# Rubric de codificación — Atlas Iberoamericano del Lenguaje Claro

**Estado:** v1 (P1). Sujeto a revisión tras la doble codificación del 20% (P6) si Krippendorff's α < 0.67.

## Cómo usar esta rúbrica

- Cada **pilar** tiene 3 indicadores (a, b, c). Cada indicador se puntúa 0–4.
- Un nivel se alcanza cuando su criterio observable está satisfecho **y respaldado por al menos un registro verificado** (`data/processed/records/`) con `fuente_file_id` + `cita`. Sin registro verificado, la puntuación es 0 o `insufficient_evidence` (nunca se infiere ni se estima).
- Los niveles son acumulativos: para puntuar N hay que cumplir también los criterios de N-1, N-2, etc., salvo que se indique lo contrario.
- "Vinculante" significa que existe una obligación legal exigible (no una recomendación, guía de buenas prácticas o compromiso voluntario sin consecuencias).
- "Nacional" excluye iniciativas puramente municipales, de un único organismo o de una sola universidad, salvo que el indicador lo permita explícitamente en niveles bajos.

## Alcance: entidades no soberanas

Puerto Rico (PRI) se documenta con ficha propia, mapas y anexos, pero **no se incluye en el índice numérico agregado ni en el semáforo comparativo entre países** (`country_universe.csv: incluir_en_indice_numerico=false`), porque los indicadores de Leyes e Instituciones asumen potestad legislativa y administrativa nacional propia, de la que PRI carece por su estatus de territorio no incorporado de EEUU. Sus registros sí alimentan Proyectos, Formación, Academia, Herramientas y Ciudadanía si hay evidencia, con nota metodológica explicando por qué no se compara 1:1 con países soberanos.

## Escala general (referencia; ver anclas específicas por indicador abajo)

```
0 = sin evidencia tras búsqueda documentada
1 = aislado / simbólico / puntual
2 = existe pero no vinculante, parcial o subnacional
3 = nacional, institucionalizado, vinculante o casi
4 = nacional, vinculante, dotado de recursos y evaluado
```

---

## Pilar 1. Leyes

### 1a. Estatuto vinculante de lenguaje claro

| Nivel | Ancla observable |
|---|---|
| 0 | No se encuentra, tras búsqueda documentada en boletines/diarios oficiales y bases de datos legislativas, ninguna norma que mencione lenguaje claro, llano, ciudadano o comprensible. |
| 1 | Existe una mención simbólica (ej. un considerando, una declaración de principios, una moción parlamentaria no aprobada) sin fuerza normativa propia. |
| 2 | Existe una norma (decreto, resolución, circular administrativa) que promueve el lenguaje claro pero es de rango subnacional, sectorial muy acotado, o explícitamente no vinculante ("se recomienda", "se sugiere"). |
| 3 | Existe una ley o decreto de rango nacional, publicado en el boletín/diario oficial, que establece una obligación de usar lenguaje claro en al menos un ámbito de la administración pública, con verbo de mandato ("deberá", "es obligatorio"). |
| 4 | El estatuto nacional vinculante del nivel 3 tiene, además, mecanismo de cumplimiento identificable (autoridad de supervisión, plazo de implementación, sanción o vía de reclamación) documentado en un registro separado. |

### 1b. Deber incorporado en ley sectorial (justicia, consumo, salud, procedimiento administrativo)

| Nivel | Ancla observable |
|---|---|
| 0 | Ninguna ley sectorial revisada (códigos de procedimiento, leyes de protección al consumidor, leyes de salud, leyes de acceso a la justicia) menciona claridad o comprensibilidad del lenguaje. |
| 1 | Una única ley sectorial contiene una mención aislada (ej. un artículo que pide "lenguaje sencillo" en un formulario específico) sin desarrollo reglamentario. |
| 2 | Al menos una ley sectorial nacional incorpora un deber de claridad, pero sin definición operativa (no dice qué cuenta como "claro") ni remisión a un estándar. |
| 3 | Al menos dos ámbitos sectoriales distintos (de justicia, consumo, salud o procedimiento administrativo) tienen deber de lenguaje claro con alguna definición operativa o remisión a una guía/norma. |
| 4 | Tres o más ámbitos sectoriales con deber de lenguaje claro vinculante, y al menos uno de ellos cuenta con jurisprudencia, reglamento de desarrollo o resolución administrativa que lo haya aplicado en un caso concreto. |

### 1c. Normas privadas/sectoriales + mecanismo de cumplimiento

| Nivel | Ancla observable |
|---|---|
| 0 | No se identifica ninguna norma privada, código de autorregulación sectorial (banca, seguros, telecomunicaciones) ni certificación relacionada con lenguaje claro. |
| 1 | Existe una norma privada o código de conducta sectorial que menciona el lenguaje claro como recomendación, sin adhesión verificable de empresas. |
| 2 | Existe una norma privada/sectorial con adhesión voluntaria documentada de al menos una entidad, pero sin mecanismo de verificación ni consecuencias por incumplimiento. |
| 3 | Existe un esquema sectorial (ej. de un regulador financiero o de consumo) con adhesión de múltiples entidades y algún mecanismo de verificación (auditoría, sello, reporte). |
| 4 | El esquema del nivel 3 tiene mecanismo de cumplimiento con consecuencias reales documentadas (sanción, retiro de sello, resolución de un ente regulador) en al menos un caso registrado. |

---

## Pilar 2. Instituciones

### 2a. Unidad/oficina pública dedicada

| Nivel | Ancla observable |
|---|---|
| 0 | No se identifica ninguna unidad, oficina, comisión o cargo con mandato explícito de lenguaje claro en ningún organismo público. |
| 1 | Existe una persona o rol informal (ej. un "referente" designado dentro de un área de comunicación) sin estructura ni presupuesto propio, o una unidad extinta/temporal. |
| 2 | Existe una unidad formal dentro de un único organismo (ej. un ministerio o un tribunal), con mandato documentado pero sin alcance intersectorial. |
| 3 | Existe una unidad u oficina de alcance nacional o intersectorial (ej. adscrita a la presidencia, a la función pública o al poder judicial en su conjunto) con mandato formal y personal dedicado. |
| 4 | La unidad del nivel 3 tiene presupuesto propio identificable y produce informes o entregables periódicos verificables (guías, evaluaciones, memorias anuales). |

### 2b. Red o comisión nacional

| Nivel | Ancla observable |
|---|---|
| 0 | No existe ninguna red, comisión o mesa de trabajo interinstitucional sobre lenguaje claro. |
| 1 | Ha existido una reunión o mesa puntual (una sola vez, sin continuidad) documentada. |
| 2 | Existe una red o comisión activa pero de composición limitada (un solo sector o un número reducido de instituciones), sin acta de creación formal. |
| 3 | Existe una comisión o red nacional formalmente constituida (decreto, resolución o acta fundacional) con participación multisectorial (más de un poder del Estado o más de un sector). |
| 4 | La red/comisión del nivel 3 tiene reuniones periódicas documentadas (más de una, en fechas distintas) y produce resultados conjuntos verificables (guías compartidas, recomendaciones, informes). |

### 2c. Penetración en poder judicial / redacción legislativa

| Nivel | Ancla observable |
|---|---|
| 0 | No se encuentra evidencia de iniciativas de lenguaje claro dentro del poder judicial ni en técnica legislativa. |
| 1 | Iniciativa puntual y aislada (una sentencia reescrita como ejercicio, un curso único) sin continuidad institucional. |
| 2 | Existe una iniciativa sostenida dentro de un tribunal o cámara legislativa específicos (no todo el poder judicial ni todo el legislativo), sin mandato formal. |
| 3 | Existe un mandato formal (acordada, reglamento interno, manual de técnica legislativa) que aplica a todo un poder del Estado (todo el poder judicial de un país, o el proceso de redacción legislativa nacional). |
| 4 | El mandato del nivel 3 tiene evidencia de aplicación medible: sentencias o leyes efectivamente redactadas o reescritas en lenguaje claro conforme al mandato, documentadas con casos concretos. |

---

## Pilar 3. Proyectos

### 3a. Programa o plan de gobierno

| Nivel | Ancla observable |
|---|---|
| 0 | No se identifica ningún programa, plan o política pública con lenguaje claro como componente. |
| 1 | El lenguaje claro aparece mencionado como objetivo dentro de un plan más amplio (ej. un plan de gobierno digital o de transparencia) sin líneas de acción propias. |
| 2 | Existe un programa o plan piloto de lenguaje claro impulsado por un organismo, de duración limitada o alcance sectorial. |
| 3 | Existe un programa de gobierno (nacional, con nombre propio, presupuesto o resolución de creación) dedicado específicamente al lenguaje claro con alcance intersectorial. |
| 4 | El programa del nivel 3 continúa activo más allá de un cambio de gobierno o gestión (evidencia de continuidad plurianual documentada), o ha sido institucionalizado mediante norma. |

### 3b. Proyectos sectoriales sostenidos

| Nivel | Ancla observable |
|---|---|
| 0 | No se registra ningún proyecto sectorial de lenguaje claro (guías, rediseño de formularios, campañas). |
| 1 | Se registra un único proyecto sectorial, ya finalizado, sin continuidad. |
| 2 | Se registran 2-3 proyectos sectoriales en el país (distintos organismos o sectores), no necesariamente coordinados entre sí. |
| 3 | Se registran 4 o más proyectos sectoriales, incluyendo al menos dos sectores distintos entre justicia, salud, administración, consumo o finanzas. |
| 4 | Los proyectos del nivel 3 muestran continuidad temporal (evidencia de actividad en al menos dos años distintos, no consecutivos en una sola ráfaga) y abarcan tres o más sectores. |

### 3c. Evidencia de evaluación/monitoreo

| Nivel | Ancla observable |
|---|---|
| 0 | Ningún proyecto registrado incluye evaluación de resultados o monitoreo. |
| 1 | Un proyecto menciona intención de evaluar (ej. "se medirá el impacto") sin resultados publicados. |
| 2 | Existe un informe de evaluación de al menos un proyecto, con metodología no especificada o muy básica (ej. encuesta de satisfacción sin metodología documentada). |
| 3 | Existe al menos una evaluación con metodología explícita (pre/post, comprobación de comprensión, testing con usuarios) y resultados publicados. |
| 4 | Existen evaluaciones metodológicamente sólidas de más de un proyecto, o una evaluación que se repite en el tiempo (seguimiento longitudinal) con resultados publicados y accesibles. |

---

## Pilar 4. Publicaciones

### 4a. Guía(s) de estilo nacional(es) oficial(es)

| Nivel | Ancla observable |
|---|---|
| 0 | No se identifica ninguna guía o manual de lenguaje claro de origen oficial. |
| 1 | Existe una guía producida por un organismo público específico, sin adopción ni difusión más allá de ese organismo. |
| 2 | Existe una guía de alcance más amplio (ej. recomendada para todo un ministerio o poder del Estado) pero de aplicación no obligatoria. |
| 3 | Existe una guía de estilo oficial de alcance nacional (aprobada por norma, decreto o resolución de alto nivel) para la administración pública en general. |
| 4 | La guía del nivel 3 tiene evidencia de actualización periódica (más de una versión documentada) o de adopción formal por múltiples organismos (listado de adherentes verificable). |

### 4b. Adopción de ISO 24495-1:2023 o norma equivalente

| Nivel | Ancla observable |
|---|---|
| 0 | No hay mención de ISO 24495-1 ni de una norma técnica nacional equivalente sobre lenguaje claro. |
| 1 | Se menciona la norma ISO en un documento (ej. una guía la cita como referencia) sin adopción formal. |
| 2 | Existe una norma técnica nacional propia sobre lenguaje claro (equivalente funcional a la ISO) o un anteproyecto de adopción de la ISO en trámite. |
| 3 | La ISO 24495-1:2023 (u otra norma equivalente formalmente reconocida) ha sido adoptada como norma nacional por el organismo nacional de normalización. |
| 4 | La adopción del nivel 3 es exigida o referenciada en al menos una norma legal o contrato público (evidencia de uso normativo, no solo de existencia). |

### 4c. Requisito de testeo con usuarios

| Nivel | Ancla observable |
|---|---|
| 0 | Ninguna guía o proyecto documentado menciona testeo con usuarios finales. |
| 1 | Una guía recomienda el testeo con usuarios como buena práctica, sin metodología ni obligatoriedad. |
| 2 | Existe evidencia de testeo con usuarios realizado en al menos un proyecto, de forma puntual y no estandarizada. |
| 3 | Existe un requisito formal (en una guía oficial o norma) de testear documentos con usuarios antes de su publicación, con metodología de referencia. |
| 4 | El requisito del nivel 3 tiene evidencia de cumplimiento sistemático en más de un organismo (informes de testeo publicados, no solo la obligación en el papel). |

---

## Pilar 5. Formación

### 5a. Cursos / certificación

| Nivel | Ancla observable |
|---|---|
| 0 | No se identifica ninguna oferta formativa en lenguaje claro. |
| 1 | Existe un curso puntual (edición única, sin repetición documentada), de cualquier proveedor. |
| 2 | Existe oferta formativa recurrente (más de una edición) de un proveedor privado o de una única institución. |
| 3 | Existe oferta formativa recurrente de alcance nacional, incluyendo al menos un programa universitario (grado, posgrado o formación continua acreditada) o una certificación reconocida por el sector público. |
| 4 | Existe una certificación formal (con evaluación y credencial verificable) reconocida por múltiples instituciones o por el Estado, con evidencia de personas certificadas. |

### 5b. Congresos o encuentros recurrentes

| Nivel | Ancla observable |
|---|---|
| 0 | No se registra ningún congreso, jornada o encuentro sobre lenguaje claro en el país. |
| 1 | Se registra un único encuentro, sin evidencia de continuidad. |
| 2 | Se registran encuentros en más de una ocasión, pero organizados por la misma entidad sin ampliar alcance. |
| 3 | Existe un encuentro o congreso nacional recurrente (al menos 2 ediciones documentadas en años distintos) con participación de múltiples instituciones. |
| 4 | El encuentro del nivel 3 tiene proyección internacional documentada (participación de otros países, o el país ha sido sede de un encuentro panhispánico/iberoamericano) en más de una edición. |

### 5c. Asociación profesional

| Nivel | Ancla observable |
|---|---|
| 0 | No existe ninguna asociación, colectivo o red profesional de lenguaje claro en el país. |
| 1 | Existe un colectivo informal (grupo de redes sociales, comunidad sin personería jurídica) sin actividad documentada más allá de su existencia. |
| 2 | Existe una asociación formalmente constituida (con estatutos o registro), de actividad reciente o reducida. |
| 3 | Existe una asociación profesional activa con actividad sostenida (eventos, publicaciones o membresía documentada en más de un año). |
| 4 | La asociación del nivel 3 participa en redes internacionales (PLAIN, Clarity, REDLAD u otra red panhispánica/iberoamericana) con evidencia de esa afiliación. |

---

## Pilar 6. Academia

### 6a. Grupos de investigación / cátedras

| Nivel | Ancla observable |
|---|---|
| 0 | No se identifica ningún grupo de investigación, cátedra o línea de investigación dedicada al lenguaje claro. |
| 1 | Un/a investigador/a individual trabaja el tema sin grupo formalmente constituido. |
| 2 | Existe un grupo de investigación reconocido por una universidad, con actividad documentada pero de alcance limitado. |
| 3 | Existe un grupo de investigación o cátedra con reconocimiento formal (registro institucional, financiamiento) y producción sostenida. |
| 4 | Existen dos o más grupos de investigación en instituciones distintas del país, o un grupo con proyección internacional (colaboraciones documentadas con otros países). |

### 6b. Publicaciones y tesis

| Nivel | Ancla observable |
|---|---|
| 0 | No se identifica ninguna publicación académica, tesis, TFM o TFG sobre lenguaje claro del país. |
| 1 | Se identifica una única publicación o tesis. |
| 2 | Se identifican 2-4 publicaciones o tesis, de cualquier nivel académico. |
| 3 | Se identifican 5 o más publicaciones/tesis, incluyendo al menos una en una revista indexada o repositorio institucional verificable. |
| 4 | La producción del nivel 3 incluye publicaciones en revistas internacionales indexadas o tesis doctorales, con evidencia de citación o impacto (referenciadas por otros trabajos). |

### 6c. Redes académicas

| Nivel | Ancla observable |
|---|---|
| 0 | No hay evidencia de participación académica del país en redes de investigación sobre lenguaje claro. |
| 1 | Participación puntual de un/a investigador/a en un evento de red internacional, sin vínculo institucional. |
| 2 | Vínculo institucional documentado (convenio, membresía) de una universidad del país con una red, sin actividad conjunta verificable. |
| 3 | Participación activa y documentada (proyectos conjuntos, publicaciones compartidas) en una red académica nacional o internacional. |
| 4 | El país coordina o ha sido sede de una red académica iberoamericana/panhispánica sobre lenguaje claro, con evidencia documental. |

---

## Pilar 7. Herramientas

### 7a. Métricas de legibilidad validadas para el idioma nacional

| Nivel | Ancla observable |
|---|---|
| 0 | No se identifica ninguna métrica de legibilidad adaptada o validada para el/los idioma(s) del país. |
| 1 | Se usa una métrica diseñada para otro idioma (ej. Flesch original en inglés) sin adaptación documentada. |
| 2 | Existe una adaptación de una métrica de legibilidad al español/portugués/criollo haitiano (ej. Fernández-Huerta, Szigriszt-Pazos, Gulpease en portugués) usada en el país, sin validación empírica local documentada. |
| 3 | Existe una métrica validada empíricamente para el idioma con estudios de correlación con comprensión lectora, publicados. |
| 4 | La métrica del nivel 3 está integrada en herramientas o normas de uso extendido en el país (evidencia de uso institucional, no solo académico). |

### 7b. Corpus/datasets de simplificación

| Nivel | Ancla observable |
|---|---|
| 0 | No existe ningún corpus o dataset de simplificación textual del idioma nacional disponible públicamente. |
| 1 | Existe un corpus de tamaño reducido o de acceso restringido, mencionado en un trabajo académico. |
| 2 | Existe un corpus de acceso público (aunque sea pequeño) documentado con ficha técnica (tamaño, fuente, licencia). |
| 3 | Existe un corpus de tamaño sustancial (miles de pares texto original/simplificado o equivalente) publicado con licencia abierta. |
| 4 | El corpus del nivel 3 ha sido usado para entrenar o evaluar herramientas de simplificación automática, con evidencia de esa aplicación (paper, modelo publicado). |

### 7c. Herramienta pública desplegada (incl. basada en LLM)

| Nivel | Ancla observable |
|---|---|
| 0 | No se identifica ninguna herramienta pública (web, API, plugin) de apoyo al lenguaje claro del país. |
| 1 | Existe un prototipo o proyecto piloto no desplegado públicamente (demo interna, paper sin herramienta accesible). |
| 2 | Existe una herramienta pública desplegada (accesible online) de origen privado o académico, sin adopción institucional. |
| 3 | Existe una herramienta pública desplegada con adopción por al menos un organismo público o gran institución. |
| 4 | La herramienta del nivel 3 tiene evidencia de uso medido (número de usuarios, documentos procesados, o integración oficial en un flujo de trabajo administrativo) documentada. |

---

## Pilar 8. Ciudadanía

### 8a. Resultados de comprensión medidos

| Nivel | Ancla observable |
|---|---|
| 0 | No existe ningún estudio que mida comprensión lectora de textos administrativos/legales por parte de la ciudadanía. |
| 1 | Existe un estudio de comprensión con metodología no documentada o muestra muy reducida (estudio de caso anecdótico). |
| 2 | Existe un estudio de comprensión con metodología documentada pero de alcance limitado (una institución, una muestra pequeña). |
| 3 | Existe un estudio de comprensión con metodología robusta (muestra representativa, comparación antes/después o entre versiones) de alcance nacional o multi-institucional. |
| 4 | Existen dos o más estudios del nivel 3 en momentos distintos, permitiendo comparación temporal, o el país participa en una medición internacional comparable (ej. PIAAC) con datos de comprensión de textos administrativos. |

### 8b. Deberes de lectura fácil / accesibilidad cognitiva

| Nivel | Ancla observable |
|---|---|
| 0 | No existe ninguna norma o iniciativa de lectura fácil o accesibilidad cognitiva en el país. |
| 1 | Existe una iniciativa puntual de lectura fácil (una publicación adaptada) sin marco normativo. |
| 2 | Existe una guía o norma técnica de lectura fácil, de aplicación voluntaria o de alcance institucional limitado. |
| 3 | Existe un deber legal (ley o decreto nacional) de proveer información en formato de lectura fácil o accesible cognitivamente en al menos un ámbito (ej. información electoral, de salud o de justicia). |
| 4 | El deber del nivel 3 tiene evidencia de cumplimiento verificable (documentos oficiales en lectura fácil efectivamente publicados y localizables). |

### 8c. Incidencia de sociedad civil

| Nivel | Ancla observable |
|---|---|
| 0 | No se identifica ninguna organización de sociedad civil (de personas con discapacidad, de consumidores, de derechos digitales) que haya abogado por el lenguaje claro en el país. |
| 1 | Se identifica una mención o declaración de una organización de sociedad civil sobre el tema, sin campaña o acción sostenida. |
| 2 | Existe una campaña o acción puntual de una organización de sociedad civil (informe, denuncia, petición) documentada. |
| 3 | Existe incidencia sostenida (más de una acción en el tiempo) de al menos una organización, con evidencia de interlocución con el Estado (participación en una mesa, comisión o consulta pública). |
| 4 | La incidencia del nivel 3 tiene resultado verificable atribuible (una norma, política o proyecto que cite explícitamente la incidencia de la organización como antecedente). |

---

## Registro de decisiones metodológicas de esta versión

- 2026-07-13: v1 creada tras resolver §2 del plan (universo, marco, pilares 7-8, licencia). Ver `atlas/metodologia.qmd` para el detalle completo de cada decisión y su justificación.
- Todas las anclas de nivel 4 exigen evidencia adicional respecto al nivel 3, no solo "más de lo mismo": la intención es que el salto 3→4 siempre dependa de un registro distinto (aplicación medida, actualización, adopción externa), no de una apreciación cualitativa del codificador.
- Pendiente de P6: revisar anclas donde la doble codificación muestre desacuerdo sistemático (posible ambigüedad en la redacción, no en el criterio).
