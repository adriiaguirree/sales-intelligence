# Notas y contrato provisional de datos

Última verificación: 2026-10-26

## Fuente y archivo verificados

- Ruta local: `data/Online Retail.xlsx`
- Hoja: `Online Retail`
- Filas del libro: 541,910, incluido el encabezado
- Filas de datos esperadas según la inspección: 541,909
- Columnas: 8

Procedencia documentada en el README: dataset [Online Retail de UCI](https://archive.ics.uci.edu/dataset/352/online%2Bretail), publicado por Daqing Chen con DOI `10.24432/C5BW33` y licencia CC BY 4.0. El Excel permanece como entrada inmutable, fuera de Git, y debe obtenerse desde la fuente oficial.

## Esquema observado

| Columna | Uso actual | Tipo esperado por el código | Observaciones pendientes |
|---|---|---|---|
| `InvoiceNo` | facturas únicas | identificador/cadena | Investigar convención de cancelaciones. |
| `StockCode` | no usado | identificador/cadena | Posible análisis por producto. |
| `Description` | no usado | texto | Puede contener faltantes o texto no normalizado. |
| `Quantity` | unidades y revenue | numérico | Valores negativos se interpretan como devoluciones/cancelaciones. |
| `InvoiceDate` | agrupación mensual | fecha/hora | Zona horaria y granularidad no confirmadas. |
| `UnitPrice` | filtro, revenue y media | numérico | El código excluye precios no positivos. |
| `CustomerID` | clientes y primera compra | identificador nullable | No tratar como medida numérica ni exponer valores. |
| `Country` | no usado | categoría/texto | Posible segmentación geográfica. |

## Reglas observadas en el script

Estas reglas describen el comportamiento existente; requieren confirmación analítica:

1. Se excluyen filas con `UnitPrice <= 0`.
2. `Revenue` se calcula como `Quantity * UnitPrice`.
3. `Month` se deriva de `InvoiceDate` con periodicidad mensual.
4. Las cantidades positivas contribuyen a “ventas positivas”.
5. Las cantidades negativas contribuyen a “cancelaciones/devoluciones”.
6. Revenue mensual incluye cantidades positivas y negativas después del filtro de precio.
7. Clientes únicos ignora `CustomerID` faltante.
8. “Nuevo” significa que el mes de una transacción positiva coincide con la primera compra positiva observada de ese `CustomerID` dentro del archivo.
9. Revenue promedio por factura divide revenue neto mensual entre facturas únicas del mes.
10. Precio promedio mensual es la media simple por fila de `UnitPrice`, no ponderada por unidades.

## Riesgos analíticos que deben probarse

- El conjunto puede ser una ventana parcial; “nuevo” no equivale necesariamente a nuevo para el negocio.
- Una factura cancelada puede requerir una regla basada en `InvoiceNo`, no solo en cantidad negativa.
- Filtrar precio no positivo antes de reportar exclusiones puede ocultar problemas de calidad.
- El promedio simple de precio puede sobreponderar líneas de pocas unidades.
- Mezclar facturas de venta y devolución en el denominador puede distorsionar revenue por factura.
- `CustomerID` faltante reduce la cobertura de métricas de clientes.
- Meses parciales al inicio o final no deben compararse como meses completos sin advertencia.

## Contrato mínimo implementado

Antes del análisis, validar:

- presencia exacta de las ocho columnas esperadas;
- conversión válida de `InvoiceDate`, `Quantity` y `UnitPrice`;
- unicidad no exigida por fila, pero duplicados cuantificados;
- faltantes de `CustomerID`;
- conteos de precios y cantidades cero o negativos;
- rango temporal y meses parciales;
- número de filas descartadas por cada regla.

Las pruebas automatizadas deben usar datos sintéticos. Evita copiar filas reales o identificadores de clientes a fixtures, documentación o incidencias.

## Perfil de calidad verificado el 2026-10-26

- 541,909 filas recibidas y 2,517 con `UnitPrice <= 0`.
- 135,080 filas sin `CustomerID`.
- 10,624 filas con cantidad negativa y 9,288 cuyo `InvoiceNo` empieza con `C`.
- 1,336 filas donde prefijo `C` y cantidad negativa no coinciden.
- 5,268 duplicados exactos, cuantificados pero no eliminados sin una clave de línea confirmada.
- 83.5% del revenue positivo es atribuible a filas con `CustomerID`.
