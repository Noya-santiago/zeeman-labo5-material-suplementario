# Día 1: 1 de octubre de 2026

Primeros barridos de absorción, probablemente sin imanes.

## Configuración

- **RP** (`d1-01`): rampa de la Red Pitaya, entre −141 y −127 mV. No anotamos sus parámetros.
- **GEN** (`d1-02`): generador de funciones, de unos 100 mVpp, con un divisor de 100 Ω / 8 Ω hacia la entrada de modulación del ITC4001.
- Láser: 1,2 mA y 23,5 °C.

## Registros

- `d1-01`: fotodiodo en ch1 y rampa en ch2. La unidad del tiempo es incierta (`s?`).
- `d1-02`: fotodiodo en ch2; ch1 vacío. No registra la rampa.

Con `d1-01` estimamos la temperatura de la celda a partir del área de los pozos.
