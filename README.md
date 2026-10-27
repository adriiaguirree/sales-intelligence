# Sales Intelligence: adquisicion frente a recurrencia

Caso de estudio reproducible en Python sobre transacciones de comercio electronico.
Convierte un analisis exploratorio en un pequeño proyecto de ingenieria con validacion
de esquema, metricas probadas, controles de calidad y un reporte generado por codigo.

## Pregunta de negocio

> ¿El aumento de ventas entre septiembre y noviembre de 2011 coincide principalmente
> con clientes nuevos, clientes recurrentes o ambas cosas?

La evidencia descriptiva apunta principalmente a clientes recurrentes. De octubre a
noviembre el revenue neto aumento 36.5%; los clientes nuevos bajaron de 358 a 323 y los
recurrentes subieron de 1,006 a 1,341. En noviembre, los recurrentes aportaron 88.2% del
revenue de compras positivas con cliente identificado.

Esto no demuestra causalidad. Ademas, `New` significa primera compra positiva observada
en el archivo, no primera compra historica real.

## Que demuestra el proyecto

- separacion entre carga, validacion, transformacion, metricas y presentacion;
- reglas de negocio visibles y probadas con datos sinteticos;
- denominadores y exclusiones cuantificados;
- ejecucion independiente del directorio de trabajo;
- reporte, tablas y grafica reproducibles;
- interpretacion de negocio que distingue evidencia, inferencia y limitaciones.

## Estructura

```text
src/data_analysis.py                 CLI
src/sales_intelligence/analysis.py  reglas y metricas puras
src/sales_intelligence/pipeline.py  carga y orquestacion
src/sales_intelligence/reporting.py reporte y grafica
tests/                              pruebas con datos sinteticos
STUDY_GUIDE.md                      resumen para estudiar
outputs/                            derivados locales ignorados por Git
```

## Datos

El proyecto usa [Online Retail de UCI](https://archive.ics.uci.edu/dataset/352/online%2Bretail),
publicado por Daqing Chen, DOI `10.24432/C5BW33`, bajo licencia CC BY 4.0.
Contiene 541,909 lineas transaccionales entre el 1 de diciembre de 2010 y el 9 de
diciembre de 2011 para un comercio online del Reino Unido.

1. Descarga `Online Retail.xlsx` desde la pagina oficial.
2. Crea el directorio `data/` si no existe.
3. Guarda el archivo como `data/Online Retail.xlsx`.

El Excel esta ignorado por Git. No se modifica durante el analisis.

## Instalacion

Requiere Python 3.12, que es la version con la que se verifico esta entrega.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Ejecucion

Desde cualquier directorio:

```bash
python /ruta/al/proyecto/src/data_analysis.py
```

Tambien se pueden elegir rutas explicitas:

```bash
python src/data_analysis.py \
  --input "data/Online Retail.xlsx" \
  --output-dir outputs
```

Se generan:

- `outputs/report.md`;
- `outputs/monthly_metrics.csv`;
- `outputs/customer_segments.csv`;
- `outputs/data_quality.csv`;
- `outputs/monthly_revenue.png`.

## Pruebas

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Las pruebas no usan identificadores ni filas reales. Verifican esquema, devoluciones,
denominadores, varias compras en el primer mes y la ejecucion completa del pipeline.

## Definiciones principales

- `Revenue = Quantity * UnitPrice`.
- Revenue neto: suma de revenue en filas con `UnitPrice > 0`, incluidas cantidades
  negativas.
- Compra positiva: `Quantity > 0` y `UnitPrice > 0`.
- `New`: primera compra positiva observada del cliente y cualquier otra compra del mismo
  cliente dentro de ese primer mes.
- `Returning`: compra positiva en un mes posterior al primero observado.

La segmentacion requiere `CustomerID` y excluye devoluciones. Por tanto, no debe sumarse
como si fuera el mismo universo que el revenue neto mensual.

## Limites conocidos

- 135,080 filas no tienen `CustomerID`.
- La segmentacion cubre 83.5% del revenue positivo.
- Hay 5,268 duplicados exactos, cuantificados pero no eliminados sin una regla confirmada.
- Diciembre de 2011 solo contiene datos hasta el dia 9.
- Una relacion temporal descriptiva no prueba una causa ni justifica por si sola una
  recomendacion comercial.

Consulta [STUDY_GUIDE.md](STUDY_GUIDE.md) para repasar el razonamiento y continuar con
otro proyecto.
