# Estabilización de un láser con el efecto Zeeman en rubidio: material suplementario

Grupo 10, Laboratorio 5, FCEN-UBA, 2026.
Tomás Carnero, Abraham Machicado, Santiago Noya y Lucas Velasco.

## Contenido

- [`data/`](data/README.md): los registros de la Red Pitaya de las tres clases (58 CSV y 3 configuraciones JSON), con un índice en `data/medidas.csv`.
- [`docs/uso_lock_in.md`](docs/uso_lock_in.md): cómo usamos la aplicación lock-in+PID v0.2.2 para lockear el láser.
- [`analisis/campo_imanes.ipynb`](analisis/campo_imanes.ipynb): cómo pasamos de la separación entre los pozos de los dos canales al campo de los imanes, paso a paso.
- [`analisis/espectro_steck.ipynb`](analisis/espectro_steck.ipynb): cómo armamos el espectro D1 con los datos de Steck y el ajuste de la fracción de ⁸⁷Rb. Usa [`analisis/barridos.py`](analisis/barridos.py), que procesa los barridos como en el informe.

## Fuentes

- Aplicación lock-in+PID, de Marcelo Luda: [código](https://github.com/marceluda/rp_lock-in_pid) y [documentación](https://marceluda.github.io/rp_lock-in_pid/). Usamos la versión 0.2.2; la documentación describe la 0.2.3.
- Datos atómicos: D. A. Steck, *Rubidium 85 D Line Data* y *Rubidium 87 D Line Data*, [steck.us/alkalidata](https://steck.us/alkalidata/).
