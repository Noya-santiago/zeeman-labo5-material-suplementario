# Datos

Mediciones de absorción de la línea D1 del rubidio y estabilización del láser mediante DAVS, registradas con la Red Pitaya en tres jornadas de laboratorio. Se publican 61 CSV originales, 58 copias con nombres ordenados y 3 configuraciones JSON (también copiadas con nombres ordenados).

```
data/
├── medidas.csv      índice de todos los registros (una fila por archivo)
├── clean/           los datos con nombre ordenado, más el README de cada día
│   ├── dia1/        01/10/2026
│   ├── dia2/        22/10/2026
│   └── dia3/        29/10/2026  (incluye configs/ con los JSON de la app)
└── raw/             los CSV originales, tal como salieron de la Red Pitaya
    ├── dia1/ dia2/ dia3/
```

- **`raw/`** no se toca. Los nombres son los que quedaron en el laboratorio. Se preservan los archivos originales sin modificar sus muestras.
- **`clean/`** son copias idénticas byte a byte, solo con otro nombre. No incluye los duplicados exactos (`d2-12`, `d2-13`) ni la prueba de la mañana del día 2 (`d2-01`). Esos tres figuran en `medidas.csv` con `archivo` vacío.
- **`medidas.csv`** es la tabla que une todo: el nombre limpio (`archivo`), el original (`archivo_raw`) y lo que sabemos de cada registro.
- **`clean/diaN/README.md`** cuenta qué hicimos ese día y define los *setups*, o sea las configuraciones que no cambian de un archivo a otro (generador, rampa, divisor, corriente del láser, etc.).

## Nombre de los archivos

`<id>_<tipo>_<canales>.csv`, por ejemplo `d3-14_lockeo_error-rampaA.csv`.

- `id`: día y número de registro en orden de hora (`d3-14` = día 3, registro 14). Es la clave para buscar el archivo en `medidas.csv`.
- `tipo`: `barrido` (rampa sin realimentación), `lockeo` (el lazo agarró la línea), `intento-lockeo` (no agarró), `adquisicion` o `calibracion`.
- `canales`: qué hay en ch1 y ch2, en ese orden (`error`, `rampaA`, `pidAout`, `in1`, `davs`, etc.). Los detalles finos están en `medidas.csv`.

## Formato de los CSV

Cuatro columnas separadas por comas, con una fila de encabezado: `t1, ch1, t2, ch2`. Son los dos canales del osciloscopio de la app, cada uno con su eje de tiempo (`t1` y `t2` son iguales). El voltaje está en V. La unidad del tiempo cambia de un archivo a otro (ver más abajo) y figura en `unidad_t`.

## Columnas de `medidas.csv`

- `id`, `dia`, `hora`: identificador, fecha de la clase y hora del archivo.
- `tipo`: lo mismo que en el nombre, con tilde.
- `ch1`, `ch2`: qué señal es cada canal.
- `unidad_t`: unidad del eje de tiempo.
- `setup`: configuración común del día (definida en el README de ese día). `GEN` es el generador de funciones y `RP` / `R1` / `R2` son rampas de la Red Pitaya.
- `imanes`: si estaban puestos (días 1 y 2).
- `error_offset`, `kp`, `psr`, `ki`, `isr`, `kd`, `sat`: parámetros del PID (día 3).
- `rampa_congelada_V`: valor al que quedó la rampa durante el lock, en V.
- `lockeado`: `sí`, `no` o `probablemente no`.
- `uso`: `bueno`, `revisar`, `fallido` (intento que no anduvo, pero sirve como dato), `duplicado` o `descartar`.
- `fuente`: de dónde sale lo que dice la fila. Puede ser `cuaderno`, `nombre` (lo que dice el nombre original), `config` (un JSON exportado por la app), `RESUMEN` (análisis previos) o `dato` (lo inferimos mirando la señal). Lo que inferimos queda marcado como tal, para no confundirlo con lo que anotamos en el laboratorio.
- `notas`: observaciones.
- `?` significa que todavía no lo sabemos.

## Ojo con la unidad del tiempo

La app exporta el tiempo en la unidad que muestra el eje, pero no la escribe en el CSV. Cuando no quedó anotada, se estimó del paso entre muestras y de la duración de las rampas. Estas inferencias y sus dudas se conservan en el índice. El reloj de la Red Pitaya es de 8 ns: por ejemplo, interpretar un paso de 0,005 como µs daría 5 ns, incompatible con ese reloj. La duración de la ventana, el zoom y el redondeo de la exportación también influyen: no alcanza con aplicar una única regla automática a todos los archivos. En particular, `d1-01` y `d3-01` conservan una unidad incierta. No usarlos para tiempos absolutos sin resolverla.

## Hora de los archivos

En los días 2 y 3, la hora sale de la fecha de modificación de cada archivo, corrida +4 h. La calibramos con `config_20261029_190909…json`: su nombre dice 19:09:09 y el archivo figura a las 15:09. Git no guarda estas fechas, así que la hora queda anotada en `medidas.csv`.

## Registros del informe

Esta correspondencia se preparó con la copia del informe y los análisis disponibles al publicar los datos. La versión final del informe puede usar una selección distinta; los identificadores y archivos originales permiten comprobarla.

Los identificadores siguientes se buscan en la columna `id` de [medidas.csv](medidas.csv). Un registro puede contener varios semibarridos; la cantidad de archivos no es la de semibarridos aceptados por el análisis.

| Parte del informe | Registros |
|---|---|
| Espectro sin imanes, calibración, deriva y jitter | `d2-03` a `d2-11`, más `d2-14` (10 archivos únicos). |
| Serie de imanes: referencia sin campo | `d2-15` a `d2-19`. |
| Serie de imanes: con campo | `d2-20` a `d2-26`. |
| Serie de imanes: campo invertido | `d2-27` a `d2-31`. |
| Barridos abiertos de la DAVS | `d2-32`, `d2-33`, `d3-01`, `d3-03`, `d3-17` y `d3-20`. La figura de la DAVS calibrada usa `d3-17`. |
| Registros de lockeo de la tabla experimental | `d3-08` a `d3-16`, `d3-18`, `d3-19`, `d3-21` a `d3-24` (15 registros). |
| Comparación de estabilidad: 13 registros con error utilizable | `d3-08`, `d3-09`, `d3-11` a `d3-16`, `d3-18`, `d3-19`, `d3-21`, `d3-22` y `d3-23`. `d3-10` no registra el error; `d3-24` muestra una oscilación anómala y no entra en esta comparación. |
| Estimación de temperatura por área de absorción | `d1-01`; depende de supuestos sobre el fondo, el cero del detector y la longitud de la celda. |

También se conservan las mediciones exploratorias del día 1, la calibración del generador y los intentos fallidos de lockeo. Su presencia aquí no implica que se hayan usado en los resultados finales.

## Leer un registro en Python

Desde la raíz del repositorio, con NumPy instalado:

```python
import csv
from pathlib import Path
import numpy as np

base = Path("data")
with (base / "medidas.csv").open(encoding="utf-8", newline="") as f:
    indice = {fila["id"]: fila for fila in csv.DictReader(f)}

registro = indice["d3-14"]
ruta = base / (registro["archivo"] or registro["archivo_raw"])
t1, ch1, t2, ch2 = np.loadtxt(ruta, delimiter=",", skiprows=1).T
print(registro["ch1"], registro["ch2"], registro["unidad_t"])
# Convertir únicamente cuando la unidad está identificada sin ambigüedad.
segundos_por_unidad = {"s": 1, "ms": 1e-3, "µs": 1e-6}
t1_s = t1 * segundos_por_unidad[registro["unidad_t"]]
```

No todas las señales de la columna `ch1` son voltajes del mismo punto del circuito. Por ejemplo, en `d3-12` el error está en **ch2**, y en `d3-10` se registraron rampa e in1. Los JSON son instantáneas de configuración: no prueban por sí solos qué ajustes tenía cada registro anterior o posterior. Consultar las notas de cada jornada.
