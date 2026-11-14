"""Procesamiento de los barridos (sección Análisis de datos del informe).

Cortamos cada registro en semibarridos, calculamos su absorbancia, la pasamos
a frecuencia con los dos pozos del 85Rb y promediamos todos los semibarridos.
"""
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import medfilt

# Centros de los dos pozos del 85Rb, en MHz: promedio de las dos líneas de cada
# grupo, pesado por su intensidad (tabla de espectro_steck.ipynb).
CENTRO_F3 = -1392.8
CENTRO_F2 = 1763.5


def leer(archivo):
    """Tiempo (s) y los dos canales (V). El CSV redondea el tiempo a 1 ms, así que
    rearmamos un eje de tiempo uniforme."""
    d = np.genfromtxt(archivo, delimiter=",", skip_header=1)
    t = np.linspace(d[0, 0], d[-1, 0], len(d))
    return t, d[:, 1], d[:, 3]


def vertices(t, y):
    """Vértices de la triangular, como (tiempo, +1 si es un máximo o -1 si es un mínimo).

    Buscamos los extremos de la señal suavizada. Para ubicar cada vértice con
    precisión, ajustamos una recta a cada lado y buscamos dónde se cortan.
    """
    dt = t[1] - t[0]
    suave = medfilt(y, int(0.05 / dt) | 1)
    w = int(0.35 / dt)                       # menos que medio período (0,5 s)
    a, b = int(0.03 / dt), int(0.15 / dt)    # tramo recto a cada lado del vértice
    lista, anterior = [], None
    for i in range(w, len(t) - w):
        ventana = suave[i - w:i + w + 1]
        if suave[i] == ventana.max() and suave[i] > 0.3:
            tipo = +1
        elif suave[i] == ventana.min() and suave[i] < 0.13:
            tipo = -1
        else:
            continue
        if anterior and anterior[1] == tipo and i - anterior[0] < w:
            continue                         # el mismo vértice, otra vez
        anterior = (i, tipo)
        izq = np.polyfit(t[i - b:i - a], y[i - b:i - a], 1)
        der = np.polyfit(t[i + a:i + b], y[i + a:i + b], 1)
        lista.append(((der[1] - izq[1]) / (izq[0] - der[0]), tipo))
    return lista


def lejos(u):
    """Zonas del semibarrido lejos de los pozos, donde ajustamos el fondo."""
    return (u > 0.05) & (u < 0.3) | (u > 0.7) & (u < 0.95)


def absorbancia(u, senal):
    """A = -ln(I/I0), con I0 una recta ajustada lejos de los pozos."""
    fondo = np.polyval(np.polyfit(u[lejos(u)], senal[lejos(u)], 1), u)
    return -np.log(senal / fondo)


def semibarridos(archivo):
    """Corta un registro en semibarridos y calcula su absorbancia.

    Cada semibarrido tiene u, que va de 0 a 1 y crece con la frecuencia, y A1 y A2,
    la absorbancia de cada canal. Descartamos los que no duran 0,5 s o tienen un salto.
    """
    t, canal1, canal2 = leer(archivo)
    lista = []
    V = vertices(t, (canal1 + canal2) / 2)
    for (t0, tipo), (t1, _) in zip(V[:-1], V[1:]):
        k = (t >= t0) & (t <= t1)
        x = (t[k] - t0) / (t1 - t0)
        u = x if tipo > 0 else 1 - x         # cuando la corriente sube, la frecuencia baja
        orden = np.argsort(u)
        u, c1, c2 = u[orden], canal1[k][orden], canal2[k][orden]
        # Un salto se ve como un escalón en el fondo: lejos de los pozos, la señal
        # tiene que quedar a menos de 6 mV de una curva suave.
        senal = (c1 + c2) / 2
        suave = np.polyval(np.polyfit(u[lejos(u)], senal[lejos(u)], 2), u)
        resto = medfilt(senal - suave, 11)            # 11 puntos = 20 ms
        if abs(t1 - t0 - 0.5) < 0.01 and np.abs(resto[lejos(u)]).max() < 0.006:
            lista.append(dict(archivo=archivo.name, sentido=tipo, u=u,
                              A1=absorbancia(u, c1), A2=absorbancia(u, c2)))
    return lista


def gaussiana(x, altura, centro, ancho):
    return altura * np.exp(-0.5 * ((x - centro) / ancho) ** 2)


def centro_pozo(u, A, aprox):
    """Centro de un pozo: ajuste gaussiano alrededor del máximo cerca de aprox."""
    i = np.argmax(np.where(np.abs(u - aprox) < 0.03, A, -np.inf))
    k = np.abs(u - u[i]) < 0.022
    return curve_fit(gaussiana, u[k], A[k], p0=[A[i], u[i], 0.008])[0][1]


def calibrar(lista):
    """Agrega a cada semibarrido su eje de frecuencia, nu (MHz).

    En cada semibarrido ubicamos los dos pozos del 85Rb en el promedio de los dos
    canales, que con imanes no se corre. Promediamos la escala
    (MHz por unidad de u) entre los semibarridos de un mismo sentido, y corremos
    cada uno para que el punto medio de sus pozos caiga donde lo ubica Steck.
    """
    # Posición aproximada de los pozos: el más hondo de la mediana es F=3, y
    # F=2 es el más hondo un poco más arriba.
    ug = np.linspace(0, 1, 2001)
    for s in lista:
        s["A"] = (s["A1"] + s["A2"]) / 2
    mediana = np.median([np.interp(ug, s["u"], s["A"]) for s in lista], axis=0)
    u3 = ug[np.argmax(mediana)]
    u2 = ug[np.argmax(np.where((ug > u3 + 0.04) & (ug < u3 + 0.15), mediana, -np.inf))]
    for s in lista:
        s["u3"], s["u2"] = centro_pozo(s["u"], s["A"], u3), centro_pozo(s["u"], s["A"], u2)
    for sentido in (+1, -1):
        grupo = [s for s in lista if s["sentido"] == sentido]
        escala = np.mean([(CENTRO_F2 - CENTRO_F3) / (s["u2"] - s["u3"]) for s in grupo])
        for s in grupo:
            medio = (s["u3"] + s["u2"]) / 2
            s["nu"] = (CENTRO_F3 + CENTRO_F2) / 2 + (s["u"] - medio) * escala


NU = np.arange(-7000, 7001, 10.0)   # eje de frecuencia del promedio, en MHz


def promedio(lista, canal="A1", ancho=100):
    """Promedio gaussiano (desvío `ancho`, en MHz) de la absorbancia de un canal,
    sobre los puntos de todos los semibarridos."""
    x = np.concatenate([s["nu"] for s in lista])
    A = np.concatenate([s[canal] for s in lista])
    pesos = np.exp(-0.5 * ((NU[:, None] - x[None, :]) / ancho) ** 2)
    return pesos @ A / pesos.sum(axis=1)
