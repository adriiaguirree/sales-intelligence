# Contexto de `sales-intelligence`

Última actualización: 2026-10-26

## Problema

Construir un análisis reproducible de transacciones minoristas que explique cambios en ventas y actividad de clientes mediante métricas auditables.

## Resultado del proyecto

Un caso de estudio de portafolio en Python que una persona externa pueda instalar, ejecutar, comprender y evaluar sin depender de conversaciones privadas.

## Objetivos de aprendizaje

- Analizar datos con pandas sin perder el significado de negocio.
- Contrastar explicaciones mediante métricas con universos y denominadores explícitos.
- Practicar modularización, validación, pruebas y reproducibilidad.
- Comunicar resultados, supuestos y limitaciones.

## Estado observado

Inspeccionado el 2026-10-26:

- `src/data_analysis.py` funciona como CLI independiente del directorio actual.
- `src/sales_intelligence/` separa análisis, pipeline y reporte.
- `tests/` contiene seis pruebas sintéticas para esquema, devoluciones, conteos, revenue y ejecución completa del pipeline.
- El pipeline genera CSV, gráfica y reporte Markdown en `outputs/`.
- `README.md` documenta datos, instalación, ejecución, pruebas, definiciones y límites.
- `STUDY_GUIDE.md` conserva el razonamiento y ejercicios de autoevaluación.
- El dataset local tiene 541,909 registros y ocho columnas.
- La instalación limpia, las seis pruebas y el pipeline completo fueron verificados el 2026-10-26.
- Estos avances constituyen la versión técnica preparada para revisión y publicación.

## Pregunta analítica

> ¿El aumento de ventas entre septiembre y noviembre se relaciona principalmente con clientes nuevos, clientes recurrentes o ambos?

La evidencia descriptiva indica que en noviembre aumentaron principalmente los clientes recurrentes observados: de octubre a noviembre los nuevos bajaron de 358 a 323 y los recurrentes subieron de 1,006 a 1,341. Esto no demuestra causalidad ni equivale a retención histórica completa.

## Alcance

### Incluido

- Análisis descriptivo de transacciones.
- Validación y controles de calidad.
- Métricas mensuales y segmentación de clientes.
- Pruebas con datos sintéticos.
- Reporte, tablas y gráfica reproducibles.
- Documentación para estudio y portafolio.

### No incluido

- Pronósticos o aprendizaje automático.
- Procesamiento en tiempo real o nube.
- API, autenticación o producto multiusuario.
- Dashboard complejo e integraciones comerciales reales.

## Definición de terminado

- Instalación, pruebas y ejecución completa verificadas desde las instrucciones del README.
- Reglas principales cubiertas por pruebas sintéticas.
- Resultados reproducibles y acompañados por límites.
- Dataset fuera de Git y procedencia/licencia documentadas.
- Revisión de secretos, datos, rutas locales, archivos generados y estado Git.
- El usuario puede explicar las decisiones técnicas y analíticas principales.
- Existe una decisión explícita de publicar, mantener privado o archivar.

## Procedencia

El contexto se consolidó a partir del repositorio, la documentación del proyecto y ejecuciones locales verificadas del análisis. La estrategia general de aprendizaje e ingresos se mantiene fuera de este repositorio.
