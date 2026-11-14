# Datos

Registros de la Red Pitaya de las tres clases: 1, 22 y 29 de octubre de 2026.
Cada carpeta `diaN/` tiene un README con la configuración del montaje y el orden de las mediciones de ese día.
`medidas.csv` tiene una fila por registro.

## Archivos

Los nombres siguen el formato `<id>_<tipo>_<canales>.csv`, por ejemplo `dia3/d3-14_lockeo_error-rampaA.csv`:

- `id`: día y número de registro, en orden de hora.
- `tipo`: `barrido` (sin realimentación), `lockeo`, `intento-lockeo` (no lockeó), `adquisicion` o `calibracion`.
- `canales`: las señales de ch1 y ch2.

Cada CSV tiene 1024 filas y cuatro columnas, `t1, ch1, t2, ch2`, con `t1 = t2`.
Los voltajes están en V.
La unidad del tiempo no figura en el archivo (ver abajo).

No publicamos `d2-01`, una prueba, ni `d2-12` y `d2-13`, que son copias exactas de `d2-11`.

## Columnas de `medidas.csv`

- `id`, `dia`, `archivo`, `hora`, `tipo`.
- `ch1`, `ch2`: señal de cada canal.
- `unidad_t`: unidad del tiempo (`s`, `ms` o `µs`).
- `setup`: configuración del barrido, definida en el README de cada día. `GEN` es el generador de funciones; `RP`, `R1` y `R2` son rampas de la Red Pitaya.
- `imanes`: `sin`, `con` o `invertidos`.
- `error_offset`, `kp`, `psr`, `ki`, `isr`, `kd`, `sat`: parámetros del PID A (día 3).
- `rampa_congelada_V`: valor de la rampa durante el lockeo, en V.
- `lockeado`: `sí` o `no`.
- `uso`: `bueno`, `revisar` o `fallido` (intento sin lockeo).
- `notas`.

Un `?` marca un valor que dedujimos de la señal o que no quedó confirmado.

## Unidad del tiempo

La aplicación exporta el tiempo en la unidad que muestra el eje, pero no la escribe en el archivo.
Cuando no la anotamos, la deducimos del paso entre muestras y del período de la rampa.
En `d1-01` y `d3-01` sigue sin resolver.

## Hora

En los días 2 y 3, la hora es la fecha de modificación de cada archivo más 4 h.
Calibramos ese corrimiento con un JSON que tiene la hora de guardado en el nombre.

## Registros usados en el informe

| Parte del informe | Registros |
|---|---|
| Espectro sin imanes: regla, deriva y jitter | `d2-03` a `d2-11` y `d2-14` |
| Serie de los imanes: sin imanes | `d2-15` a `d2-19` |
| Serie de los imanes: con imanes | `d2-20` a `d2-26` |
| Serie de los imanes: invertidos | `d2-27` a `d2-31` |
| Barridos de la DAVS | `d2-32`, `d2-33`, `d3-01`, `d3-03`, `d3-17` y `d3-20` |
| Lockeos | `d3-08` a `d3-16`, `d3-18`, `d3-19` y `d3-21` a `d3-24` |
| Estabilidad del lockeo | los lockeos salvo `d3-10` (no registra el error) y `d3-24` (oscilación de 14,6 kHz) |

## Leer un registro en Python

```python
import csv
import numpy as np

with open("data/medidas.csv", encoding="utf-8") as f:
    indice = {fila["id"]: fila for fila in csv.DictReader(f)}

r = indice["d3-14"]
t, ch1, _, ch2 = np.loadtxt("data/" + r["archivo"], delimiter=",", skiprows=1).T
print(r["ch1"], r["ch2"], r["unidad_t"])
```
