# Día 3: 29 de octubre de 2026

Barridos de la DAVS, intentos de lockeo y registros con el láser lockeado.

## Configuración

- DAVS por in1. Error = in1 − offset, como entrada del PID A, con setpoint 0 y `kd = 0`.
- `ctrl A` por out2, porque out1 tenía un falso contacto. Pasa por atenuadores de 10× y 20 dB en serie, que con la carga del montaje atenúan unas 50 veces.
- Offset compensado en la rampa: unos 65 mV de la placa y unos 62 mV de los atenuadores.
- Disparo del lockeo: `Level+time Trigger` sobre el error, con el osciloscopio en `Scan floor`.
- Láser: 23,5 °C y 1,2 mA, que bajamos a 1,1 mA cerca de las 19:00. No sabemos cuál tenían `d3-11` a `d3-13`.

## Rampas

| | step | hig | low | Amplitud | Período |
|---|---:|---:|---:|---|---|
| R1 | 1234 | 913 | −3087 | 488 mVpp | 79,04 ms |
| R2 | 157 | 1159 | −3691 | 592 mVpp | 12,26 ms |

Anotamos R1, pero todos los registros son compatibles con R2, y los tres JSON la confirman.

## Series

- `d3-01` a `d3-03`: barridos de la DAVS y un intento de lockeo.
- `d3-04` a `d3-07`: intentos fallidos. La salida del PID se satura y el error no vuelve a cero.
- `d3-08` a `d3-10`: primeros lockeos, con `kp = −1000` (dividido por 64) y `ki = −29`. `d3-10` registra la rampa e in1, no el error.
- `d3-11` a `d3-16`: lockeos variando las ganancias.
- `d3-17` a `d3-22`: barridos y lockeos en distintos cruces, con `kp = −8192` (dividido por 1024) y `ki = −291`.
- `d3-23` y `d3-24`: configuración final, con offset −509, `kp = −8191` y `ki = −291`. `d3-24` muestra una oscilación de 14,6 kHz de origen desconocido.

Al final variamos la temperatura del láser lockeado: el lock se perdió en 24,7 °C al subir y en 22,4 °C al bajar. No guardamos registros de esta prueba.

## Configuraciones guardadas

| JSON | Hora | Registros |
|---|---|---|
| [config_d3-14-16_bestlock.json](configs/config_d3-14-16_bestlock.json) | 19:09 | `d3-14` a `d3-16` |
| [config_d3-17-22_serie-davs.json](configs/config_d3-17-22_serie-davs.json) | 19:23 | `d3-17` a `d3-22` |
| [config_d3-23-24_final.json](configs/config_d3-23-24_final.json) | 19:42 | `d3-23` y `d3-24` |

Cada JSON es el estado de la aplicación en el momento en que lo guardamos.
El de las 19:09 indica una escala integral de 67 ms, mientras que la pantalla mostraba 537 ms al guardar `d3-14` a `d3-16`.
