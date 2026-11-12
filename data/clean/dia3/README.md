# Día 3 — 29 de octubre de 2026

Barridos de la DAVS e intentos de estabilización, seguidos de registros con el láser lockeado. Ver [medidas.csv](../../medidas.csv) y [originales](../../raw/dia3/).

## Configuración común

- DAVS en in1; `error = in1 − offset`; PID A con entrada `error` y setpoint 0.
- `ctrl A` por **out2**, porque out1 tenía un falso contacto. Atenuadores 10× y 20 dB en serie; atenuación medida de aproximadamente 50× con la carga del montaje.
- Compensación de offset: se registraron unos 65 mV de la placa y una corrección adicional de unos 62 mV atribuida a la cadena de atenuación. Son valores específicos del montaje; comprobar el punto de medida y la atenuación antes de convertir a cuentas.
- Trigger del lock: `Level+time`, señal `error`; referencia `Scan floor`. El flanco y el signo de las ganancias se cambiaron durante las pruebas y no quedaron registrados para todos los archivos.

## Rampas

| Configuración | step | hig | low | Factor B | Amplitud indicada | Período indicado |
|---|---:|---:|---:|---:|---|---|
| R1 (anotada, sin uso confirmado) | 1234 | 913 | −3087 | 4076 | 488 mVpp | 79,04 ms |
| R2 (usada) | 157 | 1159 | −3691 | 4096 | 592 mVpp | 12,26 ms |

Los tres JSON confirman R2 para sus instantes de guardado. Los datos también son compatibles con R2 desde los primeros registros; R1 queda como anotación sin uso confirmado.

## Series

- `d3-01` a `d3-03`: barridos y un intento inicial. `d3-01` tiene unidad de tiempo sin resolver; `d3-03` registra DAVS puro (in1).
- `d3-04` a `d3-07`: intentos fallidos. La salida del PID se satura y el error no vuelve a cero.
- `d3-08` a `d3-10`: primeros locks; `kp = −1000` con divisor 64, `ki = −29` y escala integral de 537 ms. `d3-10` registra rampa e in1, no el error.
- `d3-11` a `d3-16`: variación de ganancias. El nombre «bestlock» es una etiqueta tomada en el laboratorio; no implica que todos esos ajustes sean mejores que los demás.
- `d3-17` a `d3-22`: barridos y lock en distintos cruces. Ganancias del JSON de la serie: `kp = −8192` con divisor 1024, `ki = −291`, escala integral de 67 ms.
- `d3-23` y `d3-24`: configuración final, offset −509, `kp = −8191`, `ki = −291`. `d3-24` presenta una oscilación de unos 14,6 kHz cuyo origen no se resolvió; no entra en la comparación de estabilidad de 13 registros.

En todas estas series `kd = 0`. La corriente del láser pasó de 1,2 a 1,1 mA hacia las 19:00; no está confirmada para los registros de la transición (`d3-11` a `d3-13`). La temperatura del controlador era aproximadamente 23,5 °C.

## Configuraciones guardadas

| JSON | Hora nominal | Asociación |
|---|---|---|
| [config_d3-14-16_bestlock.json](configs/config_d3-14-16_bestlock.json) | 19:09 | Serie de variación de ganancias. |
| [config_d3-17-22_serie-davs.json](configs/config_d3-17-22_serie-davs.json) | 19:23 | Cruces de la DAVS y locks. |
| [config_d3-23-24_final.json](configs/config_d3-23-24_final.json) | 19:42 | Serie final. |

Son instantáneas, no un registro continuo. En particular, el JSON de las 19:09 indica escala integral de 67 ms, mientras que los nombres de varias mediciones indican 537 ms. Se conserva la discrepancia en lugar de asignar retroactivamente el JSON a todos los registros.

Al final se varió la temperatura del láser: el lock se perdió a 24,7 °C al subir y a 22,4 °C al bajar. **No se guardaron datos de esa prueba**; esos valores provienen del cuaderno.
