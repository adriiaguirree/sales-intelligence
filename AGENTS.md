# Instrucciones de `sales-intelligence`

## Propósito

Este repositorio desarrolla un caso de estudio reproducible de análisis de ventas con Python. Es el primer proyecto activo del programa personal de aprendizaje y portafolio.

Consulta según la tarea:

- `PROJECT_CONTEXT.md` para alcance, estado y pregunta analítica.
- `DECISIONS.md` cuando una tarea dependa de definiciones previas.
- `ROADMAP.md` para prioridades y criterios de terminado.
- `DATA_NOTES.md` para esquema, reglas y riesgos del dataset.
- `LEARNING_LOG.md` y `STUDY_GUIDE.md` para resultados y aprendizaje.
- `BACKLOG.md` para tareas candidatas.

## Fuente de verdad

- Trata como **confirmado** lo marcado como tal o verificable en el repositorio.
- Trata una **observación** como estado actual, no como decisión permanente.
- No conviertas **hipótesis** en requisitos ni correlaciones en causas.
- Si código y documentación discrepan, señala el conflicto antes de cambiar una definición analítica.

## Reglas técnicas y de datos

- Lenguaje principal: Python 3.12.
- Librerías actuales: pandas, Matplotlib y openpyxl.
- Entrada local: `data/Online Retail.xlsx`.
- CLI: `src/data_analysis.py`.
- Lógica: `src/sales_intelligence/`.
- Pruebas: `tests/`, únicamente con datos sintéticos.
- Conserva el Excel original como entrada inmutable y fuera de Git.
- Si cambian métricas, valida limpieza, signos, ventana temporal, conteos únicos y denominadores.
- No incluyas secretos, identificadores reales ni salidas sensibles en commits.

## Forma de trabajo

- Preserva cambios locales preexistentes y evita refactorizaciones no relacionadas.
- Relaciona cada métrica con una pregunta de negocio.
- Registra decisiones analíticas o arquitectónicas duraderas en `DECISIONS.md`.
- Actualiza `ROADMAP.md`, `BACKLOG.md` o `LEARNING_LOG.md` cuando cambie el estado real.
- Mantén README, código, pruebas y documentación consistentes entre sí.

## Verificación

Para cambios de código, ejecuta como mínimo:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Si cambia el pipeline o el reporte, ejecuta también el análisis completo con el dataset local y revisa los artefactos de `outputs/`. Informa qué se verificó y qué quedó pendiente.

## Límites

- No añadas nube, tiempo real, aprendizaje automático, autenticación o dashboard complejo sin un requisito validado.
- No publiques ni subas el repositorio sin petición explícita.
- Antes de publicar, revisa licencia de datos, secretos, información personal, rutas locales, archivos grandes y estado Git.
