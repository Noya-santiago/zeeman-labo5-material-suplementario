# Uso de lock-in+PID v0.2.2 para estabilizar el láser

Guía del montaje DAVS del Grupo 10, Laboratorio 5, FCEN-UBA (2026). Este texto reemplaza el apéndice operativo del informe *Estabilización de un láser con el efecto Zeeman en rubidio*.

## Conexiones y recorrido de la señal

La salida de diferencia del fotodiodo balanceado (DAVS) entra por **in1**. **out2** va a la entrada de modulación de corriente del ITC4001 a través de los atenuadores. Usamos out2 porque out1 tenía un falso contacto. La atenuación de la cadena medida en nuestro montaje fue de aproximadamente 50×; medirla con la carga real antes de fijar la excursión de corriente.

```text
in1 (DAVS) → error = in1 − offset → PID A
                                      ↓
                        ctrl A = Ramp A + PID A out
                                      ↓
                         out2 → atenuadores → ITC4001
```

Para este experimento usamos el PID de la aplicación; no necesitamos la demodulación lock-in. La alineación y el balanceo óptico se describen en el informe. Antes de cerrar el lazo, comprobar que la rampa en la entrada de modulación recorra las líneas dentro del rango de corriente elegido.

Esta guía describe las partes de la aplicación **lock-in+PID** que usamos, qué hace cada una y en qué orden las usamos.
La documentación de la aplicación [de Marcelo Luda](https://marceluda.github.io/rp_lock-in_pid/) describe la versión 0.2.3, posterior a la que usamos. Puede servir para entender cada módulo, pero los pasos de esta guía corresponden a la 0.2.2.

## La interfaz

La aplicación se abre desde un navegador conectado a la misma red que la Red Pitaya. Ingresar la dirección de la placa asignada por el laboratorio y abrir **lock-in+PID**. Esta guía supone que la versión 0.2.2 ya está instalada; el [proyecto original](https://github.com/marceluda/rp_lock-in_pid) mantiene el software y las instrucciones de instalación.
Arriba tiene un osciloscopio y, debajo, los paneles del lock-in y del PID.
Muchas opciones corresponden a funciones de la FPGA que este experimento no necesita.
Usamos el generador de rampa, el PID A y el control del lockeo; no usamos los módulos de lock-in, el PID B, el sistema de relockeo (`Relock system`) ni la medición de respuesta al escalón (`Step response`).

Conviene saber cuatro cosas de la interfaz antes de empezar.
Un doble clic sobre el nombre de un campo muestra una explicación de ese campo.
Los valores se cambian más fácil con la ruedita del mouse sobre la casilla que escribiéndolos, y con Ctrl, Shift o Ctrl+Shift cambia el tamaño del paso.
La aplicación corrige sola los valores inválidos: por ejemplo, no deja que el límite bajo de la rampa supere al alto.
Por último, en los botones, oscuro significa activado y claro, desactivado.

## Osciloscopio

El osciloscopio muestra dos señales de la placa, una en cada canal (A y B), elegidas entre las entradas, la rampa, el error y las salidas de los PID.
Lo disparamos siempre con el disparo externo (`Ext Trig`) en `Scan floor`, que dispara cuando la rampa llega a su mínimo.
Así el gráfico queda quieto y el tiempo en pantalla coincide con la posición en la rampa, que es lo que usa el control del lockeo ([ver sección](#elegir-el-punto-de-lockeo)).
De los modos de disparo, el automático no espera al disparo, así que mientras la rampa barre conviene el normal.
Para la escala vertical usamos casi siempre el botón `Auto`.

## Salidas

En el panel de salidas se elige qué señal sale por out1 y por out2.
Para el lockeo importan tres señales:

- `Ramp A`, la triangular que genera la placa;

- `ctrl A`, la rampa más la salida del PID A;

- `error`, la señal que el PID lleva a cero ([ver sección](#senal-de-error-y-pid-a)).

Al láser mandamos `ctrl A`, por out2.
Mientras la rampa barre y el PID está apagado, `ctrl A` es igual a la rampa.
Al lockear, en cambio, la rampa queda congelada y el PID le suma sus correcciones.
Por eso `ctrl A` es la única de las tres que sirve tanto para barrer como para lockear.

## Rampa

La aplicación define la rampa con un límite alto `h` (`Ramp hig lim`) y un límite bajo `l` (`Ramp low lim`), en cuentas (8192 cuentas son 1 V), y con un tiempo por escalón `s`, en ciclos de reloj de 8 ns.
La rampa sube de `l` a `h` de a una cuenta, se queda `s + 1` ciclos en cada escalón, y después baja de la misma manera.
La interfaz llama a `s` `Ramp period`, aunque no es el período.
El período, la amplitud y el valor medio ideales son:

```text
período = 2 × (h − l) × (s + 1) × 8 ns
amplitud pico a pico = (h − l) / 8192 V
valor medio ideal = (h + l) / (2 × 8192) V
```

Cambiar los límites también cambia el período.
Debajo de los campos, la página muestra el período, la amplitud y el valor medio de la rampa; conviene mirar esos números después de cada cambio.
El campo `Ramp B factor` escala una segunda rampa, que no usamos.
En la mayoría de los lockeos usamos `h = 1159`, `l = −3691` y `s = 157`, con el offset ya compensado.

La rampa tiene dos casillas.
`Scan enable` la arranca y la detiene, pero al detenerla la salida no vuelve a cero: se queda en el valor en que estaba la rampa.
`Scan reset`, en cambio, lleva la rampa a cero mientras está marcada.
Además, la rampa solo corre si también está activado el botón `Scan enable` del control del lockeo ([ver sección](#control-del-lockeo)).

Para compensar el offset de la Red Pitaya seguimos estos pasos:

1. Marcamos `Scan reset` y medimos la salida con un osciloscopio. Lo que se ve es el offset de la cadena en ese punto de medida. En nuestro montaje registramos una corrección total equivalente a unos 127 mV en la escala de salida de la placa; no es un valor universal.

1. Pasamos el offset referido a la salida de la placa a cuentas, multiplicando los milivolts por 8,192, y lo restamos de `h` y de `l`. Los 127 mV son unas 1040 cuentas. Si se mide después de un atenuador, primero hay que referir la corrección a la salida de la placa usando la atenuación medida; no multiplicar directamente ese voltaje por 8,192.

1. Desmarcamos `Scan reset` y miramos la rampa en la entrada del láser. Si no quedaba centrada, corregimos los dos límites por igual hasta centrarla.

<a id="senal-de-error-y-pid-a"></a>

## Señal de error y PID A

La señal de error se arma en el selector `Error signal`: es una entrada menos un offset.
El selector empieza en "0", que no es ninguna señal, así que hay que elegir in1, donde entra la DAVS.
Para ajustar el offset pusimos el error en el canal A del osciloscopio y la rampa en el canal B.
Movimos el offset hasta que el error quedara centrado en cero, y miramos en el canal B que el cruce elegido cayera lejos de los extremos de la rampa.

En el panel del PID A elegimos el error como entrada, y ahí también se cargan las ganancias `kp`, `ki` y `kd`.
Las ganancias son enteros, y la aplicación las divide por un factor que se elige en `More options`.
Por ejemplo, si `kp` se divide por 1024, `kp = 512` equivale a una ganancia de 0,5.
Dejamos siempre `kd = 0`.
Las casillas que reinician o congelan el integrador y la salida (`Reset integral`, `freeze out` y `freeze integral`) quedaron sin marcar.

## Control del lockeo

El panel `Lock Control` tiene dos filas con los mismos botones: `Scan enable`, `PID A enable` y `PID B enable`.
La fila de arriba muestra y cambia lo que hace la placa en ese momento:

- con la rampa encendida y el PID A apagado, la placa barre;

- con la rampa apagada y el PID A encendido, el lazo está habilitado (hay que comprobar que efectivamente mantenga el lock);

- las dos cosas encendidas no tienen sentido, porque el PID se suma a una rampa que sigue barriendo.

La fila de abajo, en `config`, define en cambio el estado que la placa toma al lockear.
Antes de que la página se conecte con la placa, todos los botones aparecen oscuros, así que una captura con todo oscuro no muestra el estado real.

El lockeo se dispara cuando se cumple una condición, que se elige en `Trigger type`.
Usamos `Level+time Trigger` sobre la señal de error.
Con esta opción, la placa lockea en el primer cruce del nivel `L` que ocurre después de un tiempo `T`, contado desde el mínimo de la rampa.
La casilla `trig upward?` elige si el cruce tiene que ser subiendo o bajando.

Hay dos botones para lockear.
`Trigger lock` arma el lockeo: queda encendido mientras espera la condición y se apaga solo al lockear, y si se lo aprieta mientras espera, cancela el lockeo.
`Lock now` lockea en el acto, donde esté la rampa, así que no sirve para elegir el punto.
Al principio apretábamos los dos, pero alcanza con `Trigger lock`.

## Elegir el punto de lockeo

Con `Choose from graph` hicimos clic sobre el cruce por cero elegido en el gráfico del error, y la aplicación tomó como `T` el tiempo del clic y como `L`, el nivel.
Este tiempo solo es correcto si el osciloscopio dispara en `Scan floor`.
Con algunos zooms, además, puede dar un tiempo equivocado, así que conviene revisar el valor de `T` que muestra la página.
Cuando cambiamos `T` o `L` a mano, el lock no funcionó.

## Procedimiento completo

Con lo anterior, el orden que seguimos para lockear fue este:

1. Abrir la aplicación y elegir `ctrl A` en out2.

1. Dejar en la fila de arriba de `Lock Control` solo la rampa encendida, con los dos PID apagados. Si el PID A queda encendido, la salida no es la rampa pura.

1. Configurar la rampa y compensar el offset ([ver sección](#rampa)).

1. Elegir in1 en `Error signal` y centrar el error en cero ([ver sección](#senal-de-error-y-pid-a)).

1. En el PID A, elegir el error como entrada y cargar las ganancias.

1. En la fila de abajo de `Lock Control` (en `config`), apagar la rampa, encender el PID A y dejar apagado el PID B. Elegir `Level+time Trigger` sobre el error.

1. Elegir el cruce con `Choose from graph` ([ver sección](#elegir-el-punto-de-lockeo)).

1. Apretar `Trigger lock`. Dentro de un período de la rampa, la fila de arriba pasa a rampa apagada y PID A encendido.

1. Comprobar el lockeo con el error en el canal A y la salida del PID A en el canal B, según las comprobaciones indicadas abajo.

1. Para soltar el lock, apagar el PID A en la fila de arriba y volver a encender la rampa.

Una vez lockeado, pudimos cambiar las ganancias sin perder el lock.
Si se pierde, alcanza con volver a barrer y lockear otra vez.


## Comprobar el lock y resolver problemas

Que la rampa se congele no basta para confirmar el lock. Comprobar las tres señales:

- **Ramp A:** queda constante.

- **error:** queda cerca de cero con fluctuaciones pequeñas; tras un pequeño cambio del offset, se aparta y vuelve a cero.

- **PID A out:** corrige continuamente y no queda clavado en el límite de saturación.

El signo de `kp` y `ki` depende de la pendiente del cruce y del sentido en que responde el láser. En el experimento elegimos los valores por prueba, con `kd = 0`. Los valores guardados se documentan en [el día 3](../data/clean/dia3/README.md); no constituyen un ajuste universal del controlador.

| Síntoma | Qué revisar |
|---|---|
| La rampa no corre | `Scan reset` desmarcado y los dos `Scan enable` activados (panel de rampa y fila superior de `Lock Control`). |
| La rampa corre, pero no llega al láser | Elegir `ctrl A` en la salida física conectada al controlador. |
| `Trigger lock` queda esperando | `Scan floor`, tiempo y nivel elegidos, y flanco de `trig upward?`. Pulsarlo otra vez cancela la espera. |
| El error se aleja de cero y el PID se satura | Revisar el signo de las ganancias y el cruce elegido; soltar el lock para volver a barrer. |
| La curva está corrida verticalmente | Revisar el offset de `error` y, por separado, el offset de salida de la rampa. Son ajustes diferentes. |

## Guardar datos

Guardamos cada registro con el botón `Save Data`, que guarda lo que muestra el osciloscopio de la aplicación.
Cada archivo tiene 1024 puntos de dos canales, con una resolución de 1 mV.
La columna de tiempo está en la unidad que muestra el eje (µs, ms o s), pero el archivo no la indica. Al medir, anotar esa unidad y qué señal corresponde a cada canal. Para los registros publicados, consultar `unidad_t`, `ch1` y `ch2` en [medidas.csv](../data/medidas.csv); las unidades inciertas conservan un signo `?`.
En algunos momentos guardamos también la configuración completa de la aplicación.
