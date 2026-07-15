# Registro de adjudicación

Log de desacuerdos entre codificadores en la doble codificación del 20% (P6) y su resolución.

Formato por entrada:

```
## {iso3} — {pilar}.{indicador}
- Codificador A: {score_a} — {justificación breve}
- Codificador B: {score_b} — {justificación breve}
- Resolución: {score_final} — {razón de la adjudicación, o cambio de ancla en rubric.md si aplica}
- Fecha:
```

## Estado a 2026-07-13: P6 NO completado — no hay segundo codificador

El plan (fase P6, criterio de aceptación) exige: doble codificar una muestra aleatoria del 20% del universo (≈5 países) con un segundo codificador — Rubén, otra persona, o "an LLM coder under the identical rubric with sources attached, if documented" — y calcular Krippendorff's α (ordinal) sobre esa muestra, con objetivo ≥ 0.67.

**Esto no se ha hecho, y no se ha simulado.** Solo existe un codificador real hasta ahora: este modelo, aplicando la regla de conteo de P5 sobre el mismo conjunto de registros que él mismo extrajo en P3. Generar una "segunda codificación" con el mismo modelo sobre la misma evidencia no sería una prueba de fiabilidad independiente — mediría cuánto se repite a sí mismo el modelo, no si dos codificadores razonables llegan a la misma puntuación desde el mismo texto. Fabricar un α a partir de eso sería precisamente el tipo de apariencia de rigor sin sustancia que el plan pide evitar en todo momento ("one invented Boletín Oficial citation would discredit the whole atlas" aplica igual de bien a un coeficiente de fiabilidad inventado que a un dato inventado).

**Qué hace falta para cerrar P6 de verdad:**
1. Un segundo codificador — humano, o un modelo *distinto* al que hizo P5 (para que la comparación tenga algún valor de independencia), con acceso a `rubric.md` y a los mismos `data/processed/records/`.
2. Codificar de forma independiente (sin ver las puntuaciones de P5) una muestra aleatoria de ~5 países × 8 pilares × 3 indicadores.
3. Calcular Krippendorff's α ordinal sobre esa muestra emparejada.
4. Si α < 0.67: revisar la redacción de `rubric.md` donde haya desacuerdo sistemático, recodificar, repetir.

**Consecuencia para las fases posteriores:** el plan condiciona P9 (Study B) a que "la codificación del Atlas sea estable" — es decir, a que P6 haya pasado. Como no ha pasado, cualquier extensión del universo a ~60 países en un Estudio B se apoyaría en una codificación cuya fiabilidad nunca se verificó. Se documenta esto explícitamente en la sección de P9 de `metodologia.qmd` en vez de proceder como si el semáforo actual fuera ya un instrumento validado.
