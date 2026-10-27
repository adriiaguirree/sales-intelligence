# Registro de decisiones de `sales-intelligence`

Última actualización: 2026-10-26

## Decisiones vigentes

### D-001 — Python como lenguaje principal

- **Estado:** confirmada
- **Decisión:** desarrollar el proyecto en Python 3.12.
- **Motivo:** coincide con el objetivo técnico y el entorno verificado.

### D-002 — Contexto específico dentro del repositorio

- **Estado:** confirmada
- **Decisión:** mantener aquí el alcance, reglas de datos, decisiones y avance propios de `sales-intelligence`.
- **Consecuencia:** estrategia profesional, preferencias globales y otros proyectos viven fuera del repositorio.

### D-003 — Separar hechos, hipótesis y pendientes

- **Estado:** confirmada
- **Decisión:** no presentar inferencias como hechos ni relaciones descriptivas como causas.
- **Consecuencia:** cada conclusión importante incluye evidencia y límites.

### D-004 — Segmentación de clientes

- **Estado:** confirmada para este caso de estudio
- **Decisión:** usar compras positivas con `CustomerID`; clasificar como `New` las compras del primer mes positivo observado y como `Returning` las de meses posteriores.
- **Motivo:** devoluciones no deben definir la primera compra y varias líneas no representan varios clientes.
- **Consecuencia:** “nuevo” significa nuevo en la ventana observada, no nuevo históricamente para el negocio.

### D-005 — No eliminar duplicados sin una clave confirmada

- **Estado:** vigente
- **Decisión:** cuantificar duplicados exactos, pero no eliminarlos automáticamente.
- **Motivo:** no existe una clave de línea confirmada para distinguir errores de registros válidos repetidos.

### D-006 — Entregable y nombre operativo de la métrica

- **Estado:** confirmada para el cierre técnico solicitado el 2026-10-26
- **Decisión:** cerrar esta versión como repositorio más reporte reproducible, sin dashboard adicional, y llamar **revenue neto** a la suma de `Quantity × UnitPrice` en filas con precio positivo, incluidas cantidades negativas.
- **Motivo:** responde la pregunta analítica y produce una pieza demostrable sin añadir una interfaz que no aporta evidencia nueva.
- **Alternativas consideradas:** notebook, dashboard y API; quedan fuera hasta que un usuario o una decisión profesional los justifique.
- **Consecuencias y riesgos:** “revenue neto” es una etiqueta analítica de este caso, no una afirmación contable general. La segmentación de clientes usa otro universo y no reconcilia directamente con esta métrica.

## Observaciones actuales

| ID | Observación | Evidencia | Implicación |
|---|---|---|---|
| O-001 | Análisis, orquestación y presentación están separados | `src/sales_intelligence/` | La modularización base ya existe. |
| O-002 | Seis pruebas sintéticas y de integración pasan | `tests/` y ejecución limpia del 2026-10-26 | Las reglas y el pipeline están verificados. |
| O-003 | El Excel está ignorado por Git | `.gitignore` | Verificar que nunca haya sido versionado. |
| O-004 | Septiembre-noviembre muestran más actividad y predominio de recurrentes | ejecución y reporte | Es asociación descriptiva, no causalidad. |
| O-005 | README y guía de estudio ya describen el caso | archivos locales | Falta revisión final de consistencia y publicación. |

## Preguntas pendientes

- ¿La convención de cancelación por prefijo `C` requiere una regla adicional?
- ¿El repositorio se publicará, permanecerá privado o se archivará?

## Plantilla

```markdown
### D-NNN — Título

- **Estado:** propuesta | confirmada | reemplazada
- **Fecha:** AAAA-MM-DD
- **Decisión:**
- **Motivo:**
- **Alternativas consideradas:**
- **Consecuencias y riesgos:**
```
