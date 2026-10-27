# Guia de estudio y cierre

## 1. El proyecto en una frase

Este proyecto toma transacciones de retail, aplica reglas explicitas de limpieza y
responde si el crecimiento de septiembre a noviembre de 2011 coincide mas con
adquisicion o con recurrencia de clientes.

## 2. Recorrido del dato

```text
Excel inmutable
→ validacion de columnas y tipos
→ campos derivados (Revenue, Month, IsCancellation)
→ reglas de inclusion
→ metricas mensuales y segmentacion
→ controles de calidad
→ CSV + grafica + reporte Markdown
```

La idea central es que cada salida debe poder rastrearse hasta una regla y cada regla
critica debe tener una prueba pequena.

## 3. Conceptos de pandas que debes poder explicar

### `copy()` despues de filtrar

Crea un DataFrame independiente antes de agregar columnas. Evita modificar una vista
ambigua del original.

### `groupby(...).agg(...)`

Forma grupos y calcula varias metricas por grupo. En `monthly_metrics`, cada grupo es un
mes; se calculan revenue, unidades, facturas y clientes con denominadores diferentes.

### `nunique()`

Cuenta valores distintos. Varias lineas o facturas del mismo cliente siguen contando
como un cliente.

### `transform("min")`

Calcula la primera fecha por cliente y devuelve el resultado alineado con cada fila.
Asi cada compra puede compararse con el primer mes observado de su cliente.

### Mascara booleana

Expresiones como `(Quantity > 0) & CustomerID.notna()` hacen visible el universo exacto
de una metrica. Cambiar la mascara cambia la pregunta que responde el numero.

## 4. Reglas que debes poder defender

1. El archivo fuente no se modifica.
2. Las columnas obligatorias y tipos se validan antes de calcular.
3. Filas con `UnitPrice <= 0` no forman parte del revenue analizado.
4. Cantidades negativas reducen el revenue neto.
5. Una devolucion anterior no define la primera compra de un cliente.
6. `New` se determina con la primera compra positiva dentro de la ventana observada.
7. Varias compras del primer mes cuentan una sola vez al medir clientes nuevos.
8. Los faltantes de `CustomerID` quedan fuera de la segmentacion, pero se cuantifican.

## 5. Resultado analitico

| Mes | Revenue neto | New | Returning |
|---|---:|---:|---:|
| 2011-09 | 1,019,687.62 | 299 | 967 |
| 2011-10 | 1,070,704.67 | 358 | 1,006 |
| 2011-11 | 1,461,756.25 | 323 | 1,341 |

Entre octubre y noviembre:

- el revenue neto crecio 36.5%;
- los clientes nuevos disminuyeron 9.8%;
- los recurrentes aumentaron 33.3%;
- los recurrentes aportaron 88.2% del revenue positivo identificable de noviembre.

Conclusion defendible: el pico de noviembre coincide principalmente con mayor actividad
de clientes ya observados. Conclusion no defendible: una estrategia de retencion causo
el pico o necesariamente producira el mismo resultado en otro negocio.

## 6. Por que importan los denominadores

El revenue neto usa filas con precio positivo e incluye devoluciones. La segmentacion
usa solo compras positivas con cliente identificado. No son el mismo universo.

La cobertura identificable es 83.5% del revenue positivo. Ese porcentaje permite decir
cuanto de la actividad puede atribuirse a `New` o `Returning`, en vez de ocultar el dato
faltante.

## 7. Que prueban las pruebas

- falta una columna → error comprensible;
- devolucion antes de comprar → no convierte al cliente en `New`;
- dos compras en el primer mes → un solo cliente nuevo;
- devoluciones → reducen revenue neto;
- precio cero → queda fuera;
- pipeline sintetico → crea todos los artefactos esperados.

Las pruebas no demuestran que la definicion de negocio sea universalmente correcta.
Demuestran que el codigo implementa consistentemente la definicion elegida.

## 8. Preguntas de autoevaluacion

Intenta responder sin mirar el codigo:

1. ¿Por que `sum()` y `nunique()` responden preguntas distintas?
2. ¿Por que una devolucion no debe determinar `FirstPurchaseMonth`?
3. ¿Que cambia si `New` se define por fecha exacta en lugar de por mes?
4. ¿Por que no eliminamos automaticamente los duplicados exactos?
5. ¿Por que 88.2% no implica causalidad?
6. ¿Que sesgo introducen las filas sin `CustomerID`?
7. ¿Por que diciembre de 2011 no es comparable con noviembre?
8. ¿Que parte del pipeline puedes reutilizar y que parte depende de este dataset?

## 9. Ejercicio de reconstruccion

Para comprobar que lo aprendiste, crea sin copiar una funcion que reciba cinco compras
sinteticas de dos clientes y devuelva clientes `New` y `Returning` por mes. Luego agrega
una devolucion anterior a la primera compra y comprueba que el resultado no cambia.

## 10. Puerta antes del siguiente proyecto

El siguiente proyecto todavia no esta elegido. Primero debes poder explicar este caso y
decidir que ruta quieres probar inicialmente:

- portafolio para empleo;
- primer servicio freelance;
- exploracion de una herramienta repetible.

Esa decision cambia el usuario, el problema y el criterio de exito del Proyecto 2. Una
vez elegida, conviene seleccionar un proyecto pequeno que aporte una competencia que
este repositorio todavia no demuestre. No abras otro repositorio solo por acumular casos.
