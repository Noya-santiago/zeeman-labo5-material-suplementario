# Día 1 — 1 de octubre de 2026

Primeros barridos de absorción. Los dos registros están identificados en [medidas.csv](../../medidas.csv); los [originales](../../raw/dia1/) se conservan sin cambios.

## Configuraciones

- **RP (`d1-01`):** rampa de la Red Pitaya, medida entre −141 y −127 mV. Sus parámetros digitales no quedaron registrados. La unidad de tiempo es incierta (`s?` en el índice); no usarla como tiempo absoluto confirmado.
- **GEN (`d1-02`):** generador de funciones y divisor de 100 Ω / 8 Ω hacia el ITC4001. La amplitud del generador se estimó en unos 100 mVpp; no fue anotada. La rampa no se guardó en un canal, por lo que su forma y frecuencia se infieren de la señal.
- Corriente del láser: 1,2 mA. Temperatura del controlador: aproximadamente 23,5 °C (no es una medición de temperatura de la celda).
- Probablemente se midió sin imanes, pero no quedó confirmado.

## Uso y limitaciones

`d1-01` registra fotodiodo y rampa; en `d1-02`, el fotodiodo está en ch2 y ch1 está vacío. El índice conserva estas diferencias.

La estimación de temperatura de la celda por área de absorción procede de `d1-01`. Supone señal proporcional a la intensidad transmitida, cero oscuro nulo y un camino óptico provisional de 75 mm. No se midió el voltaje oscuro con el haz bloqueado. Es una estimación condicionada por esos supuestos.
