# Registro de aprendizaje

Última actualización: 2026-10-26

Este archivo conserva qué se aprendió y qué evidencia lo respalda. No sustituye las pruebas ni el registro de decisiones.

## Lección actual — adquisición frente a retención

### Pregunta

¿El aumento de ventas de septiembre a noviembre se relaciona con clientes nuevos, clientes recurrentes o ambos?

### Conceptos practicados

- `groupby("CustomerID")["InvoiceDate"].transform("min")` obtiene la primera fecha observada por cliente y devuelve el resultado alineado con cada fila.
- Comparar `Month` con `FirstPurchaseMonth` etiqueta operaciones del primer mes observado.
- `nunique()` evita contar varias compras del mismo cliente como varios clientes.
- Solo se usan compras positivas y `CustomerID` presente para esta segmentación.

### Resultados verificados

Ejecución local de `src/data_analysis.py` el 2026-10-26:

| Mes | Revenue neto | Unidades | Facturas únicas | Clientes únicos | Nuevos | Recurrentes |
|---|---:|---:|---:|---:|---:|---:|
| 2011-09 | 1,019,687.622 | 563,391 | 2,170 | 1,302 | 299 | 967 |
| 2011-10 | 1,070,704.670 | 598,860 | 2,402 | 1,425 | 358 | 1,006 |
| 2011-11 | 1,461,756.250 | 741,886 | 3,210 | 1,710 | 323 | 1,341 |

Los conteos `New + Returning` son menores que `clientes únicos` porque la segmentación usa únicamente compras positivas, mientras que el conteo general incluye todas las cantidades después del filtro de precio. Es una diferencia intencional entre universos y se explica en el README y en el reporte generado.

### Interpretación provisional

- Los tres meses combinan clientes nuevos y recurrentes.
- En cada mes predominan los recurrentes.
- De octubre a noviembre, el aumento de recurrentes es mucho mayor que el de nuevos; de hecho, nuevos baja de 358 a 323 mientras recurrentes sube de 1,006 a 1,341.
- Esto sugiere que la actividad de clientes ya observados es una parte importante del pico de noviembre.
- No demuestra una causa ni permite hablar de retención histórica real: el dataset solo revela recurrencia dentro de su ventana.

### Interpretación cerrada con revenue por segmento

- En noviembre, `Returning` aporta 1,025,225.26 y `New` aporta 136,592.12 entre compras positivas con cliente identificado.
- `Returning` representa 88.2% de ese revenue identificable de noviembre.
- La segmentación cubre 83.5% del revenue positivo total del dataset.
- De octubre a noviembre, el revenue neto aumenta 36.5%, `New` baja de 358 a 323 y `Returning` sube de 1,006 a 1,341.

Conclusión defendible: el pico de noviembre coincide principalmente con actividad de clientes ya observados. Esto no demuestra causalidad ni valida por sí solo una inversión comercial en retención.

### Limitaciones que el análisis debe decir en voz alta

- `New` significa “primera compra positiva observada en el archivo”.
- Faltan identificadores para una parte material de las transacciones.
- El precio medio actual es una media simple por línea y puede no representar el precio efectivo por unidad vendida.
- Diciembre de 2010 y diciembre de 2011 pueden ser meses parciales.
- Facturas con devoluciones y cancelaciones necesitan una definición formal.

## Método de mentoría que funcionó

1. Observar una tendencia de revenue.
2. Proponer explicaciones: precio, unidades, facturas o clientes.
3. Añadir una métrica que discrimine entre explicaciones.
4. Pedir al usuario una interpretación inicial.
5. Afinar la conclusión y declarar límites.
6. Solo entonces elegir la siguiente pregunta o cambio de código.

Cuando los fragmentos acumulados hagan difícil seguir el archivo, consolidar primero una versión completa y ejecutable.

## Lección de ingeniería — del script al pipeline

- Separar funciones puras permite probar reglas sin cargar el Excel completo.
- Una prueba demuestra que el código implementa una definición; no que la definición sea universalmente correcta.
- El pipeline conserva la entrada y escribe derivados en `outputs/`, ignorado por Git.
- Los denominadores son parte de la métrica: revenue neto, revenue positivo identificado, clientes únicos y clientes compradores no representan el mismo universo.
- Los problemas de calidad se cuantifican; no se corrigen de forma silenciosa.
