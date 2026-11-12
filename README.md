# Estabilización de un láser con el efecto Zeeman en rubidio

Material suplementario del informe del Grupo 10 de Laboratorio 5, Facultad de Ciencias Exactas y Naturales, Universidad de Buenos Aires (2026).

**Autores:** Tomás Carnero, Abraham Machicado, Santiago Noya y Lucas Velasco.

## Contenido

1. **[Uso de lock-in+PID v0.2.2](docs/uso_lock_in.md):** conexiones, rampa, señal de error, PID, elección del cruce, procedimiento de lockeo y guardado de datos. Reemplaza el apéndice operativo del informe.
2. **[Datos experimentales](data/README.md):** 61 registros CSV de las tres jornadas, 3 configuraciones JSON de la aplicación y un índice que identifica canales, unidades, condiciones y limitaciones de cada medición. Se conservan también los intentos fallidos y los duplicados, identificados en el índice.
3. **Modelo de la línea D1 del rubidio:** pendiente de incorporación. Esta primera versión publica la guía y los datos; todavía no incluye el código del modelo ni los notebooks de análisis.

## Consultar o descargar los datos

Abrir primero [data/README.md](data/README.md) y [data/medidas.csv](data/medidas.csv). Los nombres ordenados están en `data/clean/`; los originales, en `data/raw/`. **`clean` solo cambia los nombres: no filtra ni modifica las muestras.**

Se puede descargar todo con **Code → Download ZIP**, o clonar el repositorio:

```bash
git clone https://github.com/Noya-santiago/zeeman-labo5-material-suplementario.git
```

La [relación entre los registros y el informe](data/README.md#registros-del-informe) permite encontrar cada serie. Los valores desconocidos o inferidos se señalan en los metadatos; no todos los archivos son mediciones válidas para todos los análisis.

## Fuentes

La aplicación **lock-in+PID** es de Marcelo Luda: [código original](https://github.com/marceluda/rp_lock-in_pid) y [documentación](https://marceluda.github.io/rp_lock-in_pid/). Usamos la versión 0.2.2; la documentación en línea describe una versión posterior.

Los datos atómicos usados en el informe provienen de Daniel A. Steck, *Rubidium 85 D Line Data* y *Rubidium 87 D Line Data*, disponibles en [Alkali D Line Data](https://steck.us/alkalidata/). Son referencias bibliográficas, distintas de los datos experimentales publicados aquí.

## Citar este material

Tomás Carnero, Abraham Machicado, Santiago Noya y Lucas Velasco (2026). *Estabilización de un láser con el efecto Zeeman en rubidio: material suplementario*. https://github.com/Noya-santiago/zeeman-labo5-material-suplementario

Para identificar exactamente los archivos utilizados, acompañar la referencia con el identificador del commit descargado.
