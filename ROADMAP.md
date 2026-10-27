# Hoja de ruta de `sales-intelligence`

Última actualización: 2026-10-26

## Estado actual

- La pregunta analítica principal tiene una respuesta descriptiva documentada.
- El código ya está dividido en análisis, pipeline, reporte y CLI.
- Hay pruebas sintéticas, controles de calidad y artefactos reproducibles.
- README y guía de estudio están desarrollados.
- Los avances actuales conforman una versión técnica revisada y reproducible.

## Fase 1 — Análisis exploratorio

**Estado:** realizado.

- Revenue, unidades, facturas, clientes y segmentación mensual implementados.
- Periodo septiembre-noviembre interpretado con límites.

## Fase 2 — Ingeniería reproducible

**Estado:** completada y verificada.

- Responsabilidades separadas en módulos.
- Rutas configurables e independientes del directorio actual.
- Validación de esquema y controles de calidad.
- Pruebas con datos sintéticos.
- Salidas guardadas como CSV, gráfica y reporte.

**Criterio de salida:** pruebas y pipeline completo pasan desde una instalación documentada.

Cumplido el 2026-10-26: instalación limpia, seis pruebas y pipeline sobre 541,909 filas completados correctamente.

## Fase 3 — Revisión de aprendizaje

**Estado:** en revisión.

- Confirmar que el usuario puede explicar las reglas de `STUDY_GUIDE.md`.
- Completar el ejercicio de reconstrucción sin copiar.
- Resolver o aceptar explícitamente las preguntas pendientes de `DECISIONS.md`.

**Criterio de salida:** el usuario explica las decisiones centrales y reconstruye una métrica clave con datos sintéticos.

## Fase 4 — Preparación para publicación

**Estado:** revisión técnica completada; publicación pendiente de decisión del usuario.

- Ejecutar pruebas y análisis completo siguiendo el README.
- Revisar outputs, enlaces, comandos y cifras documentadas.
- Confirmar que el Excel no esté versionado.
- Revisar secretos, información personal, rutas locales y archivos grandes.
- Revisar cambios y construir un historial Git comprensible.
- Decidir repositorio público, privado o archivado.

**Criterio de salida:** una persona externa puede comprender, instalar o revisar el caso de forma segura y reproducible.

## Próximo hito

Estudiar `STUDY_GUIDE.md`, explicar las decisiones centrales y decidir si el repositorio se conserva privado, se publica o se archiva. Si se publica con permiso de reutilización, elegir también una licencia para el código. Después se puede elegir la ruta profesional inicial y seleccionar el Proyecto 2.
