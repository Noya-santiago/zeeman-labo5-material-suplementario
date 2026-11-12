# Día 2 — 22 de octubre de 2026

Barridos sin imanes, con imanes y con imanes invertidos; después, barridos de la DAVS e intentos de lockeo. Ver [medidas.csv](../../medidas.csv) y [originales](../../raw/dia2/).

## Configuraciones

- **GEN:** generador en alta impedancia, triangular simétrica de 1 Hz, 1 Vpp y offset nulo. Divisor de 22 kΩ / 100 Ω (21,87 kΩ medidos para la resistencia mayor). Las señales out+ y out− del fotodiodo entran por in1 e in2. Corriente del láser: 1,2 mA; los nombres originales indican 23,6 °C de temperatura del controlador.
- **RP:** rampa de la aplicación con `step = 450`, `hig = 2436`, `low = −4000`. Valores indicados por la interfaz: 786 mVpp, −95,5 mV de valor medio y 46,44 ms de período. Salida por out1. Estos barridos usaron el divisor resistivo, no la cadena de atenuadores del día 3.

## Orden de las mediciones

1. Prueba inicial `d2-01` y calibración del generador `d2-02`.
2. Serie sin imanes `d2-03` a `d2-14`.
3. Serie consecutiva: sin imanes `d2-15` a `d2-19`, con imanes `d2-20` a `d2-26`, invertidos `d2-27` a `d2-31`.
4. Ajuste de la lámina λ/4 y registros de DAVS/lockeo `d2-32` a `d2-35`.

La lámina se giró **después** de la serie de imanes. La comparación SIN/CON/CON− conserva la misma polarización.

## Limitaciones y duplicados

- `d2-11`, `d2-12` y `d2-13` son idénticos byte a byte. Solo `d2-11` tiene copia en esta carpeta; todos están en `raw/`. La prueba `d2-01` tampoco se duplicó en `clean/`.
- En `d2-32`, ch1 es DAVS (in1) y ch2 es **ctrl A**, no una segunda señal de absorción. La salida presenta un recorte y una amplitud cuya causa no quedó determinada.
- `d2-34` muestra una transición y oscilaciones; su nombre informal no confirma un lock estable. Los canales se identificaron a partir de las señales.
- En los intentos de lockeo se usaron `kp = 688`, `ki = 4`, `kd = 0`, según las anotaciones reconstruidas. Los ajustes no equivalen por sí solos a una medición de estabilidad.
- Las unidades de tiempo y su grado de certeza están en el índice. Las horas son reconstruidas a partir de los archivos, como se explica en [la descripción de los datos](../../README.md).
