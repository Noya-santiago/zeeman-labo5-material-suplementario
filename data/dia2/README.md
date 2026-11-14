# Día 2: 22 de octubre de 2026

Espectros sin imanes, con imanes y con los imanes invertidos; después, barridos de la DAVS y primeros intentos de lockeo.

## Configuración

- **GEN**: generador en alta impedancia, triangular simétrica de 1 Hz, 1 Vpp y offset nulo, con un divisor de 22 kΩ / 100 Ω hacia el ITC4001. Los canales out+ y out− del fotodiodo entran por in1 e in2.
- **RP**: rampa de la Red Pitaya por out1, con `step = 450`, `hig = 2436` y `low = −4000` (786 mVpp, −95,5 mV de valor medio, 46,44 ms de período), con el mismo divisor.
- Láser: 1,2 mA y 23,6 °C.

## Orden de las mediciones

1. `d2-02`: calibración del generador.
2. `d2-03` a `d2-14`: espectros sin imanes.
3. Serie de los imanes, medida seguida: sin imanes (`d2-15` a `d2-19`), con imanes (`d2-20` a `d2-26`) e invertidos (`d2-27` a `d2-31`).
4. `d2-32` a `d2-35`: barridos de la DAVS e intentos de lockeo.

Giramos la lámina λ/4 después de la serie de los imanes, así que sus tres condiciones tienen la misma polarización.

## Notas

- En `d2-32`, ch2 es `ctrl A`, no una segunda señal de absorción.
- En los intentos de lockeo usamos `kp = 688`, `ki = 4` y `kd = 0`.
